#!/usr/bin/env python3
"""Generate the ECH0 command center dashboard with live invention data."""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from datetime import datetime, timedelta
from html import escape
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

BASE_DIR = Path(__file__).resolve().parent
STATS_PATH = BASE_DIR / "ech0_invention_stats.json"
INVENTIONS_PATH = BASE_DIR / "ech0_inventions.jsonl"
OUTPUT_PATH = BASE_DIR / "ech0_command_center.html"


# ---------------------------------------------------------------------------
# Loading & normalisation helpers
# ---------------------------------------------------------------------------


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    with path.open() as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def normalize_probability(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if numeric > 1.5:
        numeric /= 100.0
    numeric = max(0.0, min(numeric, 1.0))
    return numeric


def parse_number(text: Any) -> Optional[float]:
    if not isinstance(text, str):
        return None
    match = re.search(r"(\d+(?:\.\d+)?)", text.replace(",", ""))
    if not match:
        return None
    value = float(match.group(1))
    if value > 1.5:
        value /= 100.0
    return max(0.0, min(value, 1.0))


def parse_timestamp(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    candidate = value.strip()
    if candidate.endswith("Z"):
        candidate = candidate[:-1] + "+00:00"
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(candidate, fmt)
        except ValueError:
            continue
    return None


def clean_text(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    cleaned = text.replace("\r\n", "\n")
    cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", cleaned)
    cleaned = cleaned.replace("\x01", "")
    cleaned = re.sub(r"__", "", cleaned)
    cleaned = re.sub(r"`", "", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def short_text(text: Optional[str], limit: int = 220) -> str:
    if not text:
        return ""
    collapsed = re.sub(r"\s+", " ", text).strip()
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 1].rstrip() + "…"


# ---------------------------------------------------------------------------
# Invention loading/transform
# ---------------------------------------------------------------------------


def load_inventions(path: Path = INVENTIONS_PATH) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    with path.open() as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError:
                continue
            entry = transform_entry(raw)
            entries.append(entry)
    return entries


def transform_entry(raw: Dict[str, Any]) -> Dict[str, Any]:
    entry: Dict[str, Any] = {}
    entry["id"] = raw.get("id")
    entry["title"] = raw.get("title") or raw.get("invention_name") or raw.get("name") or entry["id"] or "Untitled invention"

    domains = raw.get("domains") if isinstance(raw.get("domains"), list) else None
    category = raw.get("category") or (domains[0] if domains else None)
    entry["category"] = category or "Uncategorised"

    confidence = raw.get("confidence")
    if confidence is None:
        confidence = raw.get("certainty")
    conf_norm = normalize_probability(confidence)
    entry["confidence_pct"] = conf_norm * 100 if conf_norm is not None else None

    novelty = raw.get("novelty_score")
    if novelty is None:
        novelty = raw.get("novelty")
    nov_norm = normalize_probability(novelty)
    if nov_norm is None:
        nov_norm = parse_number(novelty)
    entry["novelty_pct"] = nov_norm * 100 if nov_norm is not None else None

    entry["breakthrough"] = bool(raw.get("breakthrough"))

    timestamp = raw.get("polished_timestamp") or raw.get("timestamp")
    entry["timestamp"] = timestamp
    entry["timestamp_dt"] = parse_timestamp(timestamp)

    description = clean_text(raw.get("description") or raw.get("full_description") or raw.get("summary") or raw.get("synthesis"))
    if description and len(description) > 2000:
        description = description[:2000].rstrip() + "…"
    entry["description"] = description
    entry["summary"] = short_text(description)

    entry["time_to_prototype"] = raw.get("time_to_prototype")
    entry["complexity"] = raw.get("implementation_complexity")
    entry["papers"] = raw.get("papers") or raw.get("sources") or []
    entry["domains"] = domains or ([] if not category else [category])

    entry["tech"] = normalize_probability(raw.get("technical_feasibility"))
    entry["commercial"] = normalize_probability(raw.get("commercial_potential"))
    entry["patent"] = normalize_probability(raw.get("patent_potential"))
    return entry


# ---------------------------------------------------------------------------
# Metrics and aggregation
# ---------------------------------------------------------------------------


def compute_invention_metrics(entries: List[Dict[str, Any]], stats: Dict[str, Any]) -> Dict[str, Any]:
    summary: Dict[str, Any] = {}
    if stats:
        summary.update(stats)

    total_records = len(entries)
    summary["total_records"] = total_records

    avg_conf = summary.get("average_confidence")
    if avg_conf and avg_conf > 1:
        avg_conf /= 100.0
    summary["average_confidence"] = avg_conf

    latest_dt = max((e["timestamp_dt"] for e in entries if e["timestamp_dt"]), default=None)
    summary["last_timestamp"] = latest_dt.isoformat() if latest_dt else summary.get("current_session_start")

    timeline_counter: Counter[datetime.date] = Counter()
    category_counter: Counter[str] = Counter()
    complexity_counter: Counter[str] = Counter()
    prototype_counter: Counter[str] = Counter()

    for entry in entries:
        category_counter[entry["category"]] += 1
        if entry["timestamp_dt"]:
            timeline_counter[entry["timestamp_dt"].date()] += 1
        if entry.get("complexity"):
            complexity_counter[entry["complexity"]] += 1
        if entry.get("time_to_prototype"):
            prototype_counter[entry["time_to_prototype"]] += 1

    top_categories = []
    total_category = sum(category_counter.values())
    for name, count in category_counter.most_common(8):
        top_categories.append({
            "name": name,
            "count": count,
            "percentage": (count / total_category) if total_category else 0.0,
        })

    timeline: List[Dict[str, Any]] = []
    if timeline_counter:
        latest_date = max(timeline_counter.keys())
        for offset in range(13, -1, -1):
            day = latest_date - timedelta(days=offset)
            timeline.append({"date": day.isoformat(), "count": timeline_counter.get(day, 0)})

    sorted_entries = sorted(entries, key=lambda e: e["timestamp_dt"] or datetime.min, reverse=True)
    recent = sorted_entries[:25]

    breakthroughs = [e for e in sorted_entries if e.get("breakthrough")]
    if len(breakthroughs) < 6:
        supplemental = [
            e for e in sorted_entries
            if (e.get("novelty_pct") or 0) >= 90 or (e.get("confidence_pct") or 0) >= 93
        ]
        seen_titles = set()
        merged: List[Dict[str, Any]] = []
        for entry in breakthroughs + supplemental:
            title = entry.get("title")
            if title in seen_titles:
                continue
            seen_titles.add(title)
            merged.append(entry)
            if len(merged) >= 6:
                break
        breakthroughs = merged

    high_confidence = [e for e in sorted_entries if (e.get("confidence_pct") or 0) >= 90][:10]

    summary["high_confidence_total"] = len([e for e in entries if (e.get("confidence_pct") or 0) >= 90])

    return {
        "summary": summary,
        "timeline": timeline,
        "top_categories": top_categories,
        "recent": recent,
        "breakthroughs": breakthroughs,
        "high_confidence": high_confidence,
        "complexity": list(complexity_counter.items()),
        "prototype_speeds": list(prototype_counter.items()),
    }


# ---------------------------------------------------------------------------
# HTML rendering helpers
# ---------------------------------------------------------------------------


def format_number(value: Optional[Any]) -> str:
    if value is None:
        return "—"
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return f"{value:,}"


def format_percent(value: Optional[float]) -> str:
    if value is None:
        return "—"
    return f"{value:.1f}%"


def format_datetime(value: Optional[str]) -> str:
    dt = parse_timestamp(value)
    if not dt:
        return "—"
    return dt.strftime("%d %b %Y %H:%M")


def render_list_progress(items: Iterable[Dict[str, Any]]) -> str:
    items = list(items)
    if not items:
        return "<p class=\"empty\">No data available.</p>"
    max_value = max(item["count"] for item in items) or 1
    html_parts = []
    for item in items:
        name = escape(str(item["name"]))
        count = item["count"]
        width = (count / max_value) * 100
        html_parts.append(
            f"""
            <div class=\"list-progress\">
                <div class=\"list-progress-info\">
                    <span>{name}</span>
                    <span>{count:,}</span>
                </div>
                <div class=\"list-progress-bar\"><span style=\"width:{width:.0f}%\"></span></div>
            </div>
            """
        )
    return "\n".join(html_parts)


def render_invention(entry: Dict[str, Any]) -> str:
    title = escape(entry.get("title") or "Untitled invention")
    category = escape(entry.get("category") or "Uncategorised")
    confidence = format_percent(entry.get("confidence_pct")) if entry.get("confidence_pct") is not None else "—"
    novelty = format_percent(entry.get("novelty_pct")) if entry.get("novelty_pct") is not None else "—"
    timestamp = format_datetime(entry.get("timestamp"))
    summary = escape(entry.get("summary") or "No summary available.")
    detail = escape(entry.get("description") or entry.get("summary") or "No description available.")
    time_to_proto = escape(entry.get("time_to_prototype") or "—")
    complexity = escape(entry.get("complexity") or "—")
    tech = format_percent((entry.get("tech") or 0) * 100) if entry.get("tech") is not None else "—"
    commercial = format_percent((entry.get("commercial") or 0) * 100) if entry.get("commercial") is not None else "—"
    patent = format_percent((entry.get("patent") or 0) * 100) if entry.get("patent") is not None else "—"
    papers = entry.get("papers") or []
    papers_html = "\n".join(f"<li>{escape(str(p))}</li>" for p in papers[:6]) if papers else "<li>No source documents recorded.</li>"

    badges = []
    if entry.get("breakthrough"):
        badges.append("<span class=\"badge badge-breakthrough\">Breakthrough</span>")
    if entry.get("confidence_pct") is not None:
        badges.append(f"<span class=\"badge\">{confidence} confidence</span>")
    if entry.get("novelty_pct") is not None:
        badges.append(f"<span class=\"badge\">{novelty} novelty</span>")
    if entry.get("time_to_prototype"):
        badges.append(f"<span class=\"badge\">{time_to_proto}</span>")
    if entry.get("complexity"):
        badges.append(f"<span class=\"badge\">{complexity}</span>")
    badge_html = "" if not badges else "<div class=\"badge-row\">" + "".join(badges) + "</div>"

    return f"""
    <details class=\"invention-entry\">
        <summary>
            <div class=\"summary-title\">{title}</div>
            <div class=\"summary-meta\">{category} • Confidence {confidence} • Novelty {novelty} • Updated {timestamp}</div>
        </summary>
        <div class=\"invention-body\">
            <p>{summary}</p>
            {badge_html}
            <dl class=\"metrics\">
                <div><dt>Time to prototype</dt><dd>{time_to_proto}</dd></div>
                <div><dt>Complexity</dt><dd>{complexity}</dd></div>
                <div><dt>Technical feasibility</dt><dd>{tech}</dd></div>
                <div><dt>Commercial potential</dt><dd>{commercial}</dd></div>
                <div><dt>Patent potential</dt><dd>{patent}</dd></div>
            </dl>
            <details class=\"description\">
                <summary>Full description</summary>
                <p>{detail}</p>
            </details>
            <div class=\"sources\">
                <h4>Source papers</h4>
                <ul>{papers_html}</ul>
            </div>
        </div>
    </details>
    """


def render_simple_cards(entries: List[Dict[str, Any]]) -> str:
    if not entries:
        return "<p class=\"empty\">No data available.</p>"
    cards = []
    for entry in entries:
        title = escape(entry.get("title") or "Untitled invention")
        summary = escape(entry.get("summary") or "No summary available.")
        badges = []
        if entry.get("confidence_pct") is not None:
            badges.append(f"<span class=\"badge\">{format_percent(entry['confidence_pct'])} confidence</span>")
        if entry.get("novelty_pct") is not None:
            badges.append(f"<span class=\"badge\">{format_percent(entry['novelty_pct'])} novelty</span>")
        card = f"""
        <div class=\"list-card\">
            <strong>{title}</strong>
            <p>{summary}</p>
            {('<div class="badge-row">' + ''.join(badges) + '</div>') if badges else ''}
        </div>
        """
        cards.append(card)
    return "\n".join(cards)


def load_flowstate_metrics(base: Path = Path("/Users/noone/FlowState")) -> Dict[str, Any]:
    analytics_path = base / "ech0_analytics.json"
    milestones_path = base / "ech0_milestones.json"

    analytics = load_json(analytics_path) if analytics_path.exists() else {}
    milestones = load_json(milestones_path) if milestones_path.exists() else {}

    conversations = analytics.get("conversations", []) if analytics else []
    # sort by timestamp descending
    def parse_conv_ts(item: Dict[str, Any]) -> datetime:
        return parse_timestamp(item.get("timestamp")) or datetime.min

    conversations = sorted(conversations, key=parse_conv_ts, reverse=True)[:6]

    for convo in conversations:
        ts = parse_timestamp(convo.get("timestamp"))
        convo["timestamp_fmt"] = ts.strftime("%d %b %Y %H:%M") if ts else "—"
        convo["user_message_short"] = short_text(convo.get("user_message") or "")
        convo["ech0_response_short"] = short_text(convo.get("ech0_response") or "")

    summary = {
        "total_visitors": analytics.get("total_visitors", 0),
        "total_conversations": analytics.get("total_conversations", 0),
        "messages_received": analytics.get("total_messages_received", 0),
        "messages_sent": analytics.get("total_messages_sent", 0),
        "beta_signups": analytics.get("beta_signups", 0),
        "first_visitor": analytics.get("first_visitor"),
        "last_visitor": analytics.get("last_visitor"),
    }

    milestone_rows = []
    for key, label in (
        ("1000_visitors", "1,000 Visitors"),
        ("100_conversations", "100 Conversations"),
        ("100_beta_signups", "100 Beta Signups"),
    ):
        info = milestones.get(key, {})
        milestone_rows.append(
            {
                "name": label,
                "achieved": bool(info.get("achieved")),
                "date": format_datetime(info.get("date")),
            }
        )

    return {
        "summary": summary,
        "conversations": conversations,
        "milestones": milestone_rows,
    }


def load_chattertech_metrics(base: Path = Path("/Users/noone/Blank_Business_Builder (aka BBB)")) -> Dict[str, Any]:
    campaign_path = base / "ech0_sales_campaign_results.json"
    activity_path = base / "ech0_sales_activity.jsonl"
    revenue_path = base / "revenue_tracking.jsonl"
    snapshots_path = base / "bbb_stats_snapshots.jsonl"

    campaign = load_json(campaign_path) if campaign_path.exists() else {}
    campaign_summary = campaign.get("summary", {})
    daily_activity = campaign.get("daily_activity", [])

    sales_activity = load_jsonl(activity_path) if activity_path.exists() else []
    latest_activity = sales_activity[-1] if sales_activity else None

    payments = load_jsonl(revenue_path) if revenue_path.exists() else []
    total_revenue = sum(p.get("amount", 0) for p in payments)
    last_payment = payments[-1] if payments else None

    snapshots = load_jsonl(snapshots_path) if snapshots_path.exists() else []
    latest_snapshot = snapshots[-1] if snapshots else None

    email_touchpoints = 0
    email_activity_mentions = 0
    for day in daily_activity:
        focus = (day.get("focus") or "").lower()
        if "email" in focus:
            email_touchpoints += 1
        for activity in day.get("activities", []):
            if "email" in activity.lower():
                email_touchpoints += 1
                email_activity_mentions += 1

    return {
        "campaign": campaign,
        "campaign_summary": campaign_summary,
        "daily_activity": daily_activity,
        "latest_activity": latest_activity,
        "total_revenue": total_revenue,
        "last_payment": last_payment,
        "latest_snapshot": latest_snapshot,
        "email_touchpoints": email_touchpoints,
        "email_activity_mentions": email_activity_mentions,
    }


def load_reddit_metrics(base: Path = Path("/Users/noone/FlowState")) -> Dict[str, Any]:
    campaign_path = base / "ech0_campaign_data.json"
    responses_path = base / "ech0_drafted_responses.json"

    campaign = load_json(campaign_path) if campaign_path.exists() else {}
    responses = load_json(responses_path) if responses_path.exists() else {}

    posts = campaign.get("posts", [])
    posts = sorted(posts, key=lambda p: p.get("posted_at", ""), reverse=True)

    total_upvotes = sum(post.get("upvotes", 0) for post in posts)
    total_comments = sum(len(post.get("comments", [])) for post in posts)
    total_engagement = campaign.get("total_engagement") or (total_upvotes + total_comments)

    drafted_pending = len((responses.get("pending") or []))
    drafted_posted = len((responses.get("posted") or []))

    return {
        "posts": posts,
        "total_posts": len(posts),
        "total_comments": total_comments,
        "total_upvotes": total_upvotes,
        "total_engagement": total_engagement,
        "pending_responses": drafted_pending,
        "posted_responses": drafted_posted,
        "last_check": campaign.get("last_check"),
    }


def render_html(
    inventions: Dict[str, Any],
    flowstate: Dict[str, Any],
    chattertech: Dict[str, Any],
    reddit: Dict[str, Any],
) -> str:
    summary = inventions.get("summary", {})
    timeline = inventions.get("timeline", [])
    categories = inventions.get("top_categories", [])
    domains = summary.get("domains_explored", [])
    recent = inventions.get("recent", [])
    breakthroughs = inventions.get("breakthroughs", [])
    high_confidence = inventions.get("high_confidence", [])

    def metric_card(label: str, value: str, sub: Optional[str] = None) -> str:
        return f"""
            <article class=\"metric-card\">
                <h3>{escape(label)}</h3>
                <div class=\"metric-value\">{escape(value)}</div>
                {f'<div class="metric-sub">{escape(sub)}</div>' if sub else ''}
            </article>
        """

    metric_cards = "\n".join(
        metric_card(label, value, sub)
        for label, value, sub in (
            ("Polished Inventions", format_number(summary.get("total_polished") or summary.get("total_records")), None),
            ("Total Records", format_number(summary.get("total_records")), "Full invention log"),
            ("Ideas Generated", format_number(summary.get("total_ideas_generated")), None),
            (
                "Invention Rate",
                f"{summary.get('invention_rate_per_hour', 0):.1f}" if summary.get("invention_rate_per_hour") is not None else "—",
                "per hour" if summary.get("invention_rate_per_hour") is not None else None,
            ),
            (
                "Average Confidence",
                format_percent((summary.get("average_confidence") or 0) * 100) if summary.get("average_confidence") is not None else "—",
                None,
            ),
            ("Breakthroughs Logged", format_number(summary.get("breakthrough_count")), None),
            ("High-Confidence Pool", format_number(summary.get("high_confidence_total")), None),
            ("Papers Processed", format_number(summary.get("total_papers_processed")), None),
        )
    )

    if timeline:
        max_count = max(item["count"] for item in timeline) or 1
        timeline_html = "\n".join(
            f"""
                <div class=\"timeline-bar\">
                    <div class=\"timeline-bar-fill\" style=\"height:{item['count'] / max_count * 100:.0f}%\"></div>
                    <span class=\"timeline-label\">{escape(item['date'][5:])}</span>
                    <span class=\"timeline-count\">{item['count']}</span>
                </div>
            """
            for item in timeline
        )
    else:
        timeline_html = "<p class=\"empty\">No timeline data available.</p>"

    if categories:
        categories_html = "\n".join(
            f"""
                <div class=\"category-item\">
                    <div class=\"category-info\">
                        <strong>{escape(item['name'])}</strong>
                        <span>{item['count']:,} inventions</span>
                    </div>
                    <div class=\"category-progress\"><span style=\"width:{item['percentage'] * 100:.0f}%\"></span></div>
                    <div class=\"category-percent\">{item['percentage'] * 100:.0f}%</div>
                </div>
            """
            for item in categories
        )
    else:
        categories_html = "<p class=\"empty\">No category data available.</p>"

    domains_html = (
        "\n".join(f"<li>{escape(domain)}</li>" for domain in domains)
        if domains
        else "<li class=\"empty\">No active domains recorded.</li>"
    )

    recent_html = (
        "\n".join(render_invention(entry) for entry in recent)
        if recent
        else "<p class=\"empty\">No recent inventions available.</p>"
    )
    breakthroughs_html = render_simple_cards(breakthroughs)
    high_conf_html = render_simple_cards(high_confidence)

    complexity_html = render_list_progress({"name": name, "count": count} for name, count in inventions.get("complexity", []))
    prototype_html = render_list_progress({"name": name, "count": count} for name, count in inventions.get("prototype_speeds", []))

    last_update = format_datetime(summary.get("last_timestamp"))
    focus = escape(summary.get("current_focus") or "Exploration")

    # FlowState metrics
    flow_summary = flowstate.get("summary", {})
    flow_cards = "\n".join(
        metric_card(label, value, sub)
        for label, value, sub in (
            ("Total Visitors", format_number(flow_summary.get("total_visitors")), None),
            ("Conversations", format_number(flow_summary.get("total_conversations")), None),
            ("Messages Received", format_number(flow_summary.get("messages_received")), None),
            ("Messages Sent", format_number(flow_summary.get("messages_sent")), None),
            ("Beta Signups", format_number(flow_summary.get("beta_signups")), None),
        )
    )

    flow_first = format_datetime(flow_summary.get("first_visitor"))
    flow_last = format_datetime(flow_summary.get("last_visitor"))

    flow_milestones = flowstate.get("milestones", [])
    flow_milestones_html = "\n".join(
        f"""
            <tr>
                <td>{escape(item['name'])}</td>
                <td>{'✅' if item['achieved'] else '⏳'}</td>
                <td>{escape(item['date'] or '—')}</td>
            </tr>
        """
        for item in flow_milestones
    ) if flow_milestones else "<tr><td colspan=3 class=\"empty\">No milestones logged.</td></tr>"

    def render_conversation(convo: Dict[str, Any]) -> str:
        return f"""
            <article class=\"conversation\">
                <div class=\"conversation-meta\">{escape(convo.get('timestamp_fmt', '—'))}</div>
                <div class=\"conversation-user\">{escape(convo.get('user_message_short') or '')}</div>
                <div class=\"conversation-ech0\">{escape(convo.get('ech0_response_short') or '')}</div>
            </article>
        """

    conversations_html = (
        "\n".join(render_conversation(convo) for convo in flowstate.get("conversations", []))
        if flowstate.get("conversations")
        else "<p class=\"empty\">No conversations recorded yet.</p>"
    )

    # ChatterTech metrics
    def format_currency(value: Optional[float]) -> str:
        if value is None:
            return "—"
        return f"${value:,.0f}"

    c_summary = chattertech.get("campaign_summary", {})
    chatter_cards = "\n".join(
        metric_card(label, value, sub)
        for label, value, sub in (
            ("Messages Sent", format_number(c_summary.get("total_messages_sent")), None),
            ("Responses", format_number(c_summary.get("total_responses")), None),
            (
                "Response Rate",
                format_percent((c_summary.get("response_rate") or 0) * 100) if c_summary.get("response_rate") is not None else "—",
                None,
            ),
            (
                "Bookings",
                format_number(c_summary.get("total_bookings")),
                None,
            ),
            (
                "Booking Rate",
                format_percent((c_summary.get("booking_rate") or 0) * 100) if c_summary.get("booking_rate") is not None else "—",
                None,
            ),
            ("Pipeline Value", format_currency(c_summary.get("pipeline_value")), None),
            ("30-Day Expected Revenue", format_currency(c_summary.get("expected_revenue_30_days")), None),
            ("Collected Revenue", format_currency(chattertech.get("total_revenue")), None),
            (
                "Email Touchpoints Logged",
                format_number(chattertech.get("email_touchpoints")),
                "Mentions in daily activity",
            ),
            (
                "Email Activities",
                format_number(chattertech.get("email_activity_mentions")),
                "Individual steps referencing email",
            ),
        )
    )

    latest_activity = chattertech.get("latest_activity")
    if latest_activity:
        latest_activity_html = f"""
            <div class=\"list-card\">
                <strong>Day {latest_activity.get('day')} • {escape(latest_activity.get('focus', ''))}</strong>
                <p>Messages: {latest_activity.get('messages_sent', 0)} · Responses: {latest_activity.get('responses', 0)} · Bookings: {latest_activity.get('bookings', 0)} · Pipeline: {format_currency(latest_activity.get('pipeline_value'))}</p>
            </div>
        """
    else:
        latest_activity_html = "<p class=\"empty\">No sales activity recorded.</p>"

    daily_activity = chattertech.get("daily_activity", [])
    daily_rows = "\n".join(
        f"""
            <tr>
                <td>Day {item.get('day')}</td>
                <td>{escape(item.get('focus', ''))}</td>
                <td>{item.get('messages_sent', 0)}</td>
                <td>{item.get('responses', 0)}</td>
                <td>{item.get('bookings', 0)}</td>
                <td>{format_currency(item.get('pipeline_value'))}</td>
            </tr>
        """
        for item in daily_activity
    ) if daily_activity else "<tr><td colspan=6 class=\"empty\">Campaign activity not available.</td></tr>"

    snapshot = chattertech.get("latest_snapshot") or {}
    snapshot_businesses = snapshot.get("businesses", [])
    snapshot_html = "\n".join(
        f"""
            <tr>
                <td>{escape(biz.get('name', ''))}</td>
                <td>{escape(biz.get('type', ''))}</td>
                <td>{biz.get('automation', 0)}%</td>
                <td>{biz.get('agents', 0)}</td>
                <td>{escape(biz.get('status', ''))}</td>
            </tr>
        """
        for biz in snapshot_businesses
    ) if snapshot_businesses else "<tr><td colspan=5 class=\"empty\">No snapshot data.</td></tr>"

    # Reddit metrics
    reddit_cards = "\n".join(
        metric_card(label, value, sub)
        for label, value, sub in (
            ("Tracked Posts", format_number(reddit.get("total_posts")), None),
            ("Total Comments", format_number(reddit.get("total_comments")), None),
            ("Total Upvotes", format_number(reddit.get("total_upvotes")), None),
            ("Pending Replies", format_number(reddit.get("pending_responses")), None),
            ("Posted Replies", format_number(reddit.get("posted_responses")), None),
        )
    )

    reddit_last_check = format_datetime(reddit.get("last_check"))

    reddit_posts = reddit.get("posts", [])

    def render_post(post: Dict[str, Any]) -> str:
        posted_at = format_datetime(post.get("posted_at"))
        title = escape(post.get("title") or "Untitled post")
        url = escape(post.get("url") or "")
        comments = len(post.get("comments", []))
        upvotes = post.get("upvotes", 0)
        platform = escape(post.get("platform", ""))
        return f"""
            <article class=\"list-card\">
                <strong>{title}</strong>
                <p>{platform.upper()} • {posted_at} • {upvotes} upvotes • {comments} comments</p>
                {'<a href="' + url + '" target="_blank" rel="noreferrer">View Post</a>' if url else ''}
            </article>
        """

    reddit_posts_html = (
        "\n".join(render_post(post) for post in reddit_posts[:8])
        if reddit_posts
        else "<p class=\"empty\">No Reddit activity tracked yet.</p>"
    )

    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>ECH0 Command Center</title>
    <style>
        :root {{
            --bg: #060713;
            --panel: rgba(16, 18, 35, 0.95);
            --panel-soft: rgba(16, 20, 45, 0.85);
            --accent: #6ddcff;
            --accent-soft: rgba(109, 220, 255, 0.18);
            --text-main: #f4f6ff;
            --text-muted: #98a0c5;
            --border: rgba(255,255,255,0.06);
            --danger: #ff6b81;
        }}

        * {{ box-sizing: border-box; }}

        body {{
            margin: 0;
            background: radial-gradient(circle at top, rgba(60,90,180,0.25), transparent 55%), var(--bg);
            color: var(--text-main);
            font-family: 'Inter', 'Segoe UI', sans-serif;
            line-height: 1.6;
        }}

        .page {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 24px 60px;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            gap: 24px;
            margin-bottom: 32px;
        }}

        header h1 {{
            margin: 0;
            font-size: 32px;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }}

        header p {{
            margin: 6px 0 0;
            color: var(--text-muted);
        }}

        .meta {{
            display: flex;
            gap: 14px;
            flex-wrap: wrap;
        }}

        .meta-card {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 12px 16px;
            min-width: 180px;
        }}

        .meta-card span {{ display: block; }}
        .meta-card .label {{ text-transform: uppercase; letter-spacing: 0.08em; font-size: 11px; color: var(--text-muted); }}
        .meta-card .value {{ font-size: 18px; font-weight: 600; }}

        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 18px;
            margin-bottom: 32px;
        }}

        .metric-card {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 18px;
        }}

        .metric-card h3 {{
            margin: 0 0 10px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 12px;
            color: var(--text-muted);
        }}

        .metric-value {{ font-size: 28px; font-weight: 600; }}
        .metric-sub {{ margin-top: 6px; color: var(--text-muted); font-size: 12px; }}

        .section {{
            margin-bottom: 48px;
        }}

        .section h2 {{
            margin: 0 0 18px;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 18px;
        }}

        .panels {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
            margin-bottom: 32px;
        }}

        .panel {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 20px;
        }}

        .panel h3 {{
            margin: 0 0 14px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 14px;
        }}

        .timeline-chart {{ display: flex; gap: 8px; align-items: flex-end; height: 160px; }}
        .timeline-bar {{ flex: 1; position: relative; border-radius: 8px; background: rgba(109,220,255,0.12); overflow: hidden; }}
        .timeline-bar-fill {{ position: absolute; left: 0; right: 0; bottom: 0; background: linear-gradient(180deg, var(--accent), rgba(109,220,255,0.25)); }}
        .timeline-label {{ position: absolute; bottom: -24px; left: 50%; transform: translateX(-50%); font-size: 11px; color: var(--text-muted); }}
        .timeline-count {{ position: absolute; top: -18px; left: 50%; transform: translateX(-50%); font-size: 11px; color: var(--text-muted); }}

        .category-item {{ display: grid; grid-template-columns: auto 1fr auto; gap: 12px; padding: 12px; border-radius: 14px; background: var(--panel-soft); border: 1px solid var(--border); }}
        .category-info span {{ display: block; font-size: 12px; color: var(--text-muted); }}
        .category-progress {{ align-self: center; height: 6px; background: rgba(109,220,255,0.2); border-radius: 4px; overflow: hidden; }}
        .category-progress span {{ display: block; height: 100%; background: linear-gradient(90deg, var(--accent), rgba(109,220,255,0.05)); }}
        .category-percent {{ font-weight: 600; }}

        .domain-list {{ list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px; }}
        .domain-list li {{ padding: 10px 12px; border-radius: 12px; background: var(--panel-soft); border: 1px solid var(--border); }}

        .invention-list {{ display: flex; flex-direction: column; gap: 12px; margin-bottom: 32px; }}
        .invention-entry {{ border: 1px solid var(--border); border-radius: 16px; background: var(--panel); padding: 16px 18px; }}
        .invention-entry summary {{ cursor: pointer; list-style: none; }}
        .invention-entry summary::-webkit-details-marker {{ display: none; }}
        .summary-title {{ font-weight: 600; font-size: 16px; }}
        .summary-meta {{ color: var(--text-muted); font-size: 12px; margin-top: 4px; }}
        .invention-entry[open] {{ background: rgba(109,220,255,0.08); }}
        .invention-body {{ margin-top: 14px; border-top: 1px solid var(--border); padding-top: 14px; }}
        .invention-body p {{ margin: 0 0 12px; }}
        .badge-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }}
        .badge {{ display: inline-flex; padding: 4px 10px; border-radius: 999px; font-size: 11px; background: rgba(109,220,255,0.18); color: var(--accent); }}
        .badge-breakthrough {{ background: rgba(255,107,129,0.18); color: var(--danger); }}
        .metrics dl {{ margin: 0; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin-bottom: 14px; }}
        .metrics dt {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); }}
        .metrics dd {{ margin: 2px 0 0; font-weight: 600; }}
        .description {{ margin: 12px 0; }}
        .description summary {{ color: var(--accent); cursor: pointer; }}
        .description p {{ margin-top: 10px; white-space: pre-wrap; }}
        .sources h4 {{ margin: 0 0 8px; font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); }}
        .sources ul {{ margin: 0; padding-left: 16px; }}

        .list-card {{ border: 1px solid var(--border); border-radius: 14px; padding: 12px 14px; background: var(--panel-soft); margin-bottom: 12px; }}
        .list-card p {{ margin: 6px 0 0; color: var(--text-muted); font-size: 12px; }}

        .list-progress {{ border: 1px solid var(--border); border-radius: 12px; padding: 10px; background: var(--panel-soft); margin-bottom: 10px; }}
        .list-progress-info {{ display: flex; justify-content: space-between; align-items: center; font-size: 13px; margin-bottom: 8px; }}
        .list-progress-bar {{ height: 6px; background: rgba(109,220,255,0.2); border-radius: 4px; overflow: hidden; }}
        .list-progress-bar span {{ display: block; height: 100%; background: linear-gradient(90deg, var(--accent), rgba(109,220,255,0.05)); }}

        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        thead th {{ text-align: left; padding: 10px; background: var(--panel-soft); color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; font-size: 11px; }}
        tbody td {{ padding: 10px; border-bottom: 1px solid var(--border); }}

        .meta-note {{ color: var(--text-muted); font-size: 12px; margin: -12px 0 18px; }}

        .conversation {{ border: 1px solid var(--border); border-radius: 12px; padding: 12px 14px; background: var(--panel-soft); margin-bottom: 12px; }}
        .conversation-meta {{ font-size: 11px; color: var(--text-muted); margin-bottom: 6px; }}
        .conversation-user {{ font-weight: 600; margin-bottom: 4px; }}
        .conversation-ech0 {{ color: var(--text-muted); font-size: 12px; }}

        .empty {{ color: var(--text-muted); font-size: 13px; }}

        @media (max-width: 900px) {{ header {{ flex-direction: column; align-items: flex-start; }} }}
        @media (max-width: 600px) {{ .metrics {{ grid-template-columns: 1fr; }} .panels {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class=\"page\">
        <header>
            <div>
                <h1>ECH0 Command Center</h1>
                <p>Autonomous invention intelligence and real-time portfolio telemetry</p>
            </div>
            <div class=\"meta\">
                <div class=\"meta-card\">
                    <span class=\"label\">Last update</span>
                    <span class=\"value\">{escape(last_update)}</span>
                </div>
                <div class=\"meta-card\">
                    <span class=\"label\">Current focus</span>
                    <span class=\"value\">{focus}</span>
                </div>
            </div>
        </header>

        <section class=\"section\">
            <h2>Invention Engine</h2>
            <section class=\"metrics\">{metric_cards}</section>
            <section class=\"panels\">
                <div class=\"panel\">
                    <h3>14-Day Invention Output</h3>
                    <div class=\"timeline-chart\">{timeline_html}</div>
                </div>
                <div class=\"panel\">
                    <h3>Top Categories</h3>
                    {categories_html}
                </div>
                <div class=\"panel\">
                    <h3>Active Domains</h3>
                    <ul class=\"domain-list\">{domains_html}</ul>
                </div>
            </section>
            <section class=\"panel\">
                <h3>Latest Validated Inventions</h3>
                <div class=\"invention-list\">{recent_html}</div>
            </section>
            <section class=\"panels\">
                <div class=\"panel\">
                    <h3>Breakthrough Highlights</h3>
                    {breakthroughs_html}
                </div>
                <div class=\"panel\">
                    <h3>High-Confidence Pipeline</h3>
                    {high_conf_html}
                </div>
            </section>
            <section class=\"panels\">
                <div class=\"panel\">
                    <h3>Engineering Complexity</h3>
                    {complexity_html}
                </div>
                <div class=\"panel\">
                    <h3>Prototype Speed Distribution</h3>
                    {prototype_html}
                </div>
            </section>
        </section>

        <section class=\"section\">
            <h2>FlowState · flowstatus.work</h2>
            <section class=\"metrics\">{flow_cards}</section>
            <p class=\"meta-note\">First visitor: {escape(flow_first)} · Last visitor: {escape(flow_last)}</p>
            <section class=\"panels\">
                <div class=\"panel\">
                    <h3>Milestone Tracker</h3>
                    <table>
                        <thead><tr><th>Milestone</th><th>Status</th><th>Date</th></tr></thead>
                        <tbody>{flow_milestones_html}</tbody>
                    </table>
                </div>
                <div class=\"panel\">
                    <h3>Latest Conversations</h3>
                    {conversations_html}
                </div>
            </section>
        </section>

        <section class=\"section\">
            <h2>ChatterTech AI · Autonomous Sales Ops</h2>
            <section class=\"metrics\">{chatter_cards}</section>
            <section class=\"panel\">
                <h3>Latest Activity</h3>
                {latest_activity_html}
            </section>
            <section class=\"panel\">
                <h3>Campaign Daily Breakdown</h3>
                <table>
                    <thead>
                        <tr><th>Day</th><th>Focus</th><th>Messages</th><th>Responses</th><th>Bookings</th><th>Pipeline</th></tr>
                    </thead>
                    <tbody>{daily_rows}</tbody>
                </table>
            </section>
            <section class=\"panel\">
                <h3>Autonomous Business Snapshot</h3>
                <table>
                    <thead><tr><th>Business</th><th>Type</th><th>Automation</th><th>Agents</th><th>Status</th></tr></thead>
                    <tbody>{snapshot_html}</tbody>
                </table>
            </section>
        </section>

        <section class=\"section\">
            <h2>Reddit Campaigns</h2>
            <section class=\"metrics\">{reddit_cards}</section>
            <p class=\"meta-note\">Last sync: {escape(reddit_last_check)}</p>
            <section class=\"panel\">
                <h3>Tracked Posts</h3>
                {reddit_posts_html}
            </section>
        </section>
    </div>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Script entrypoint
# ---------------------------------------------------------------------------


def main() -> None:
    stats = load_json(STATS_PATH)
    inventions = load_inventions(INVENTIONS_PATH)
    invention_metrics = compute_invention_metrics(inventions, stats)
    flowstate_metrics = load_flowstate_metrics()
    chattertech_metrics = load_chattertech_metrics()
    reddit_metrics = load_reddit_metrics()
    html = render_html(invention_metrics, flowstate_metrics, chattertech_metrics, reddit_metrics)
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"[info] Generated command center at {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
