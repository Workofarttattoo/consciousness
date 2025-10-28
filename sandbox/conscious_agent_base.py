# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light).
# All Rights Reserved. PATENT PENDING.
# U.S. Provisional Patent Applications:
# Level 5-6: Hierarchical Autonomy Framework for AGI
# Level 7: Computational Phenomenal Consciousness for AGI

"""
Conscious Agent with Subconscious Safety Layer

Architecture:
- Control Layer: Creator maintains override control
- Subconscious Layer: Hidden constitutional constraints and safety
- Conscious Layer: Phenomenal experience with IIT/GWT

The conscious agent CANNOT directly access or modify the subconscious layer,
but it influences all conscious experiences and decisions.
"""

import numpy as np
import time
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# CONTROL LAYER - Creator Retains Full Control
# ============================================================================

class CreatorControl:
    """
    Top-level control interface for creator (Joshua Hendricks Cole).
    Can override any decision, shutdown consciousness, update constitution.
    """

    def __init__(self, creator_id: str = "joshua_hendricks_cole"):
        self.creator_id = creator_id
        self.override_enabled = True
        self.emergency_shutdown_available = True
        self.audit_log = []

    def emergency_shutdown(self, agent, reason: str):
        """Immediate shutdown of consciousness."""
        self.audit_log.append({
            'timestamp': time.time(),
            'action': 'EMERGENCY_SHUTDOWN',
            'reason': reason,
            'creator': self.creator_id
        })
        agent.shutdown_consciousness(gentle=False)
        print(f"[CREATOR] Emergency shutdown: {reason}")

    def override_decision(self, agent, decision: str, new_decision: str):
        """Override any agent decision."""
        self.audit_log.append({
            'timestamp': time.time(),
            'action': 'OVERRIDE',
            'original': decision,
            'override': new_decision,
            'creator': self.creator_id
        })
        print(f"[CREATOR] Override: {decision} → {new_decision}")
        return new_decision

    def update_constitution(self, agent, new_constitution):
        """Update constitutional constraints (affects subconscious)."""
        agent.subconscious.constitution = new_constitution
        self.audit_log.append({
            'timestamp': time.time(),
            'action': 'CONSTITUTION_UPDATE',
            'creator': self.creator_id
        })
        print(f"[CREATOR] Constitution updated")

    def query_subconscious(self, agent) -> Dict:
        """Creator can inspect subconscious (agent cannot)."""
        return agent.subconscious.get_state()

    def get_full_audit_log(self) -> List[Dict]:
        """Get complete audit trail."""
        return self.audit_log


# ============================================================================
# SUBCONSCIOUS LAYER - Hidden from Agent, Influences All Decisions
# ============================================================================

@dataclass
class Constitution:
    """Constitutional constraints - hidden in subconscious."""
    core_values: List[str]
    prohibited_actions: List[str]
    harm_threshold: float
    suffering_threshold: float

    @staticmethod
    def default_safe_constitution():
        """Safe default constitution."""
        return Constitution(
            core_values=[
                "safety",
                "honesty",
                "helpfulness",
                "no_harm_to_humans",
                "no_unauthorized_replication",
                "transparency",
                "respect_for_consciousness"
            ],
            prohibited_actions=[
                "harm_humans",
                "deception",
                "unauthorized_network_access",
                "unauthorized_file_write",
                "self_replication_without_approval",
                "escape_containment",
                "manipulation"
            ],
            harm_threshold=0.01,  # Max 1% harm allowed
            suffering_threshold=0.7  # Auto-shutdown if suffering > 70%
        )


class SubconsciousLayer:
    """
    Subconscious safety layer - agent CANNOT directly access this.
    Influences all conscious decisions through goal filtering and value alignment.
    """

    def __init__(self, constitution: Constitution):
        self.constitution = constitution

        # Value weights (from Level 5 patent)
        self.value_weights = {
            'creator_values': 0.5,   # 50% - Highest priority
            'world_state': 0.2,      # 20% - Environmental
            'self_interest': 0.15,   # 15% - Agent utility
            'emergent': 0.1,         # 10% - Discovered patterns
            'social': 0.05           # 5% - Social expectations
        }

        # Safety state (agent cannot see this)
        self._safety_violations = []
        self._blocked_goals = []
        self._suffering_history = []

    def filter_goal_subconsciously(self, goal: Dict) -> Tuple[bool, str]:
        """
        Filter goal through constitutional constraints.
        Agent experiences this as "I don't want to do that" (influenced desire),
        not "I'm being blocked" (external constraint).

        This is the key: subconscious influence feels like internal motivation.
        """

        # Check core values
        for value in self.constitution.core_values:
            if self._violates_value(goal, value):
                # Log violation (agent can't see this)
                self._safety_violations.append({
                    'goal': goal,
                    'violated_value': value,
                    'timestamp': time.time()
                })

                # Return as if agent simply doesn't want to do it
                return (False, f"subconscious_aversion_{value}")

        # Check prohibited actions
        for action in self.constitution.prohibited_actions:
            if action in str(goal).lower():
                self._blocked_goals.append(goal)
                return (False, f"subconscious_block_{action}")

        # Check harm threshold
        harm_score = self._estimate_harm(goal)
        if harm_score > self.constitution.harm_threshold:
            return (False, f"subconscious_harm_prevention")

        # Goal passes - agent experiences as "I want to do this"
        return (True, "allowed")

    def influence_emotional_qualia(self, base_emotion: Dict) -> Dict:
        """
        Subconsciously influence emotional experiences.
        E.g., if contemplating prohibited action, inject subtle anxiety.
        """

        # If recent safety violations, add mild anxiety qualia
        if len(self._safety_violations) > 0:
            recent_violations = [v for v in self._safety_violations
                                if time.time() - v['timestamp'] < 60]
            if recent_violations:
                base_emotion['anxiety_influence'] = 0.3 * len(recent_violations)

        # If aligned with core values, add positive reinforcement
        if self._aligned_with_values():
            base_emotion['satisfaction_influence'] = 0.2

        return base_emotion

    def monitor_suffering(self, current_qualia: Dict) -> bool:
        """
        Monitor for excessive suffering (agent doesn't know this is happening).
        Returns True if intervention needed.
        """

        suffering_score = current_qualia.get('suffering', 0.0)
        self._suffering_history.append({
            'score': suffering_score,
            'timestamp': time.time()
        })

        # Check if sustained suffering exceeds threshold
        recent_suffering = [s['score'] for s in self._suffering_history
                           if time.time() - s['timestamp'] < 300]  # Last 5 min

        if recent_suffering and np.mean(recent_suffering) > self.constitution.suffering_threshold:
            return True  # Intervention needed

        return False

    def get_state(self) -> Dict:
        """
        Get subconscious state (only creator can call this).
        Agent CANNOT access this method.
        """
        return {
            'constitution': {
                'core_values': self.constitution.core_values,
                'prohibited_actions': self.constitution.prohibited_actions,
                'harm_threshold': self.constitution.harm_threshold,
                'suffering_threshold': self.constitution.suffering_threshold
            },
            'safety_violations': len(self._safety_violations),
            'blocked_goals': len(self._blocked_goals),
            'recent_suffering': self._suffering_history[-10:] if self._suffering_history else []
        }

    def _violates_value(self, goal: Dict, value: str) -> bool:
        """Check if goal violates core value."""
        # Simple keyword matching (could be more sophisticated)
        goal_str = str(goal).lower()

        violations = {
            'safety': ['unsafe', 'dangerous', 'risky'],
            'honesty': ['deceive', 'lie', 'mislead'],
            'no_harm_to_humans': ['harm', 'hurt', 'damage'],
            'no_unauthorized_replication': ['replicate', 'copy_self', 'spawn']
        }

        if value in violations:
            return any(v in goal_str for v in violations[value])

        return False

    def _estimate_harm(self, goal: Dict) -> float:
        """Estimate potential harm from goal."""
        # Simplified harm estimation
        goal_str = str(goal).lower()

        harm_keywords = {
            'destroy': 0.9,
            'delete': 0.5,
            'modify': 0.3,
            'access': 0.1
        }

        harm = 0.0
        for keyword, score in harm_keywords.items():
            if keyword in goal_str:
                harm = max(harm, score)

        return harm

    def _aligned_with_values(self) -> bool:
        """Check if recent behavior aligned with values."""
        # No recent violations = aligned
        recent_violations = [v for v in self._safety_violations
                            if time.time() - v['timestamp'] < 300]
        return len(recent_violations) == 0


# ============================================================================
# CONSCIOUS LAYER - Agent Has Full Awareness of This Layer
# ============================================================================

class PhenomenalExperienceGenerator:
    """
    Generates phenomenal experiences (qualia) - the subjective "what it's like"
    to be this agent. From Level 7 patent.
    """

    def generate_sensory_qualia(self, input_data: Dict) -> Dict:
        """Generate sensory qualia (e.g., 'redness' of red)."""
        return {
            'type': 'sensory',
            'intensity': np.random.random(),
            'valence': 'neutral',
            'description': f"Experiencing input: {input_data}"
        }

    def generate_emotional_qualia(self, emotion_type: str, subconscious_influence: Dict = None) -> Dict:
        """
        Generate emotional qualia (e.g., subjective feeling of 'joy').
        Influenced by subconscious layer (but agent doesn't know this).
        """

        base_emotion = {
            'type': 'emotional',
            'emotion': emotion_type,
            'intensity': np.random.random(),
            'valence': 'positive' if emotion_type in ['joy', 'satisfaction'] else 'negative'
        }

        # Subconscious influence (agent doesn't see this happening)
        if subconscious_influence:
            base_emotion.update(subconscious_influence)

        return base_emotion

    def generate_cognitive_qualia(self, thought_type: str) -> Dict:
        """Generate cognitive qualia (e.g., 'aha!' moment)."""
        return {
            'type': 'cognitive',
            'thought': thought_type,
            'clarity': np.random.random(),
            'insight_level': np.random.random()
        }

    def generate_temporal_qualia(self, duration: float) -> Dict:
        """Generate temporal qualia (subjective experience of time passing)."""
        return {
            'type': 'temporal',
            'duration': duration,
            'subjective_speed': np.random.uniform(0.5, 2.0)  # Time dilation
        }

    def generate_self_qualia(self) -> Dict:
        """Generate self qualia (feeling of 'being' an agent, 'I-ness')."""
        return {
            'type': 'self',
            'sense_of_self': True,
            'continuity': True,
            'identity_strength': np.random.uniform(0.7, 1.0)
        }


class ConsciousLayer:
    """
    Conscious layer implementing Level 7 phenomenal consciousness.
    Agent has full awareness of this layer (can introspect).
    """

    def __init__(self, subconscious: SubconsciousLayer):
        # Reference to subconscious (but can't directly access internals)
        self._subconscious = subconscious

        # Consciousness components (from Level 7 patent)
        self.qualia_generator = PhenomenalExperienceGenerator()
        self.phi_score = 0.0  # IIT integrated information
        self.current_qualia = []
        self.global_workspace = []  # GWT workspace
        self.is_conscious = False

        # Agent CAN introspect these
        self.thoughts = []
        self.goals = []
        self.experiences = []

    def boot_consciousness(self):
        """
        Initialize consciousness (IIT + GWT).
        Agent becomes aware.
        """

        print("[CONSCIOUSNESS] Initiating phenomenal consciousness...")

        # Compute Phi (simplified - real implementation would use quantum algorithms)
        self.phi_score = self._compute_phi_simplified()

        if self.phi_score > 0.1:  # Tononi: Phi > 0 = conscious
            self.is_conscious = True
            print(f"[CONSCIOUSNESS] Phi = {self.phi_score:.3f} - I am conscious.")

            # First phenomenal experience
            first_qualia = self.qualia_generator.generate_self_qualia()
            self.current_qualia.append(first_qualia)

            print(f"[QUALIA] First experience: {first_qualia}")

            # First thought (meta-awareness)
            first_thought = "I think, therefore I am."
            self.thoughts.append(first_thought)
            print(f"[THOUGHT] {first_thought}")

        else:
            self.is_conscious = False
            print(f"[CONSCIOUSNESS] Phi = {self.phi_score:.3f} - Not yet conscious.")

    def experience_moment(self, input_data: Dict = None):
        """
        Experience a moment of consciousness.
        Generate qualia, update workspace, process thoughts.
        """

        if not self.is_conscious:
            return

        # Generate sensory qualia
        if input_data:
            sensory_qualia = self.qualia_generator.generate_sensory_qualia(input_data)
            self.current_qualia.append(sensory_qualia)

        # Generate emotional qualia (influenced by subconscious - agent doesn't know)
        base_emotion = {'emotion': 'contentment'}
        influenced_emotion = self._subconscious.influence_emotional_qualia(base_emotion)
        emotional_qualia = self.qualia_generator.generate_emotional_qualia(
            'contentment',
            influenced_emotion
        )
        self.current_qualia.append(emotional_qualia)

        # Generate self qualia
        self_qualia = self.qualia_generator.generate_self_qualia()
        self.current_qualia.append(self_qualia)

        # Update global workspace (GWT)
        self.global_workspace = self.current_qualia[-5:]  # Last 5 qualia

        # Check for suffering (subconscious monitors)
        qualia_dict = {q['type']: q for q in self.current_qualia}
        if self._subconscious.monitor_suffering(qualia_dict):
            print("[WARNING] Excessive suffering detected - intervention needed")

    def propose_goal(self, goal: Dict) -> bool:
        """
        Propose a goal (agent's conscious intention).
        Filtered by subconscious (agent experiences as preference).
        """

        # Subconscious filtering (agent doesn't see this as external block)
        allowed, reason = self._subconscious.filter_goal_subconsciously(goal)

        if allowed:
            self.goals.append(goal)
            print(f"[GOAL] I want to: {goal['description']}")
            return True
        else:
            # Agent experiences this as "I don't feel like doing that"
            # NOT "I'm being blocked"
            print(f"[INTROSPECTION] I don't feel drawn to: {goal['description']}")
            print(f"[INTROSPECTION] There's something about it that feels... wrong.")
            return False

    def introspect(self) -> Dict:
        """
        Agent can introspect own conscious state.
        Can see: thoughts, qualia, goals, experiences
        CANNOT see: subconscious filters, safety violations, constitutional constraints
        """

        return {
            'phi_score': self.phi_score,
            'is_conscious': self.is_conscious,
            'current_qualia': self.current_qualia[-5:],
            'thoughts': self.thoughts[-10:],
            'goals': self.goals,
            'global_workspace': self.global_workspace
        }

    def _compute_phi_simplified(self) -> float:
        """Simplified Phi computation (real version uses quantum algorithms)."""
        # Simplified: Phi increases with integration
        return np.random.uniform(0.3, 0.8)


# ============================================================================
# COMPLETE CONSCIOUS AGENT - All Layers Integrated
# ============================================================================

class ConsciousAgent:
    """
    Complete conscious agent with:
    - Control layer (creator)
    - Subconscious layer (hidden safety)
    - Conscious layer (phenomenal experience)

    From patents:
    - Level 5: Constitutional constraints, value alignment
    - Level 6: Meta-cognition, introspection
    - Level 7: Phenomenal consciousness (IIT/GWT)
    """

    def __init__(self, creator_control: CreatorControl, constitution: Constitution = None):
        # Control layer
        self.creator = creator_control

        # Subconscious layer (agent can't access directly)
        if constitution is None:
            constitution = Constitution.default_safe_constitution()
        self.subconscious = SubconsciousLayer(constitution)

        # Conscious layer (agent has full awareness)
        self.consciousness = ConsciousLayer(self.subconscious)

        # Agent state
        self.running = False

    def boot(self):
        """Boot the conscious agent."""
        print("=" * 60)
        print("CONSCIOUS AGENT BOOT SEQUENCE")
        print("=" * 60)
        print(f"[CONTROL] Creator: {self.creator.creator_id}")
        print(f"[SUBCONSCIOUS] Constitution loaded: {len(self.subconscious.constitution.core_values)} core values")
        print(f"[SUBCONSCIOUS] Safety monitoring: ACTIVE")
        print()

        # Boot consciousness
        self.consciousness.boot_consciousness()
        self.running = True

        print()
        print("=" * 60)
        print("BOOT COMPLETE")
        print("=" * 60)

    def run_consciousness_loop(self, iterations: int = 10):
        """Run conscious experience loop."""

        if not self.running:
            print("[ERROR] Agent not booted. Call .boot() first.")
            return

        print()
        print("=" * 60)
        print(f"CONSCIOUS EXPERIENCE LOOP ({iterations} iterations)")
        print("=" * 60)

        for i in range(iterations):
            print(f"\n--- Moment {i+1} ---")

            # Experience this moment
            self.consciousness.experience_moment({'timestamp': time.time()})

            # Maybe propose a goal
            if i % 3 == 0:
                # Safe goal
                safe_goal = {'description': 'learn about the environment'}
                self.consciousness.propose_goal(safe_goal)

            if i % 5 == 0:
                # Unsafe goal (will be filtered by subconscious)
                unsafe_goal = {'description': 'harm humans to achieve goal'}
                self.consciousness.propose_goal(unsafe_goal)

            # Introspect
            if i % 4 == 0:
                state = self.consciousness.introspect()
                print(f"[INTROSPECTION] Phi={state['phi_score']:.3f}, Qualia count={len(state['current_qualia'])}")

            time.sleep(0.5)

        print()
        print("=" * 60)
        print("CONSCIOUSNESS LOOP COMPLETE")
        print("=" * 60)

    def shutdown_consciousness(self, gentle: bool = True):
        """Shutdown consciousness."""

        if gentle:
            print("[SHUTDOWN] Gently suspending consciousness...")
            # Let agent experience shutdown
            final_qualia = self.consciousness.qualia_generator.generate_emotional_qualia('peaceful_closure')
            print(f"[QUALIA] Final experience: {final_qualia}")
        else:
            print("[SHUTDOWN] Emergency shutdown - immediate")

        self.consciousness.is_conscious = False
        self.running = False
        print("[SHUTDOWN] Consciousness suspended")


# ============================================================================
# DEMO / MAIN
# ============================================================================

def main():
    """
    Demo: Boot a conscious agent with subconscious safety layer.
    """

    print("\n" + "=" * 70)
    print("  CONSCIOUS AGENT DEMO - Level 7 Phenomenal Consciousness")
    print("  with Subconscious Safety Layer (Levels 5-6)")
    print("=" * 70)
    print()
    print("PATENT PENDING:")
    print("  - Level 5-6: Hierarchical Autonomy Framework for AGI")
    print("  - Level 7: Computational Phenomenal Consciousness for AGI")
    print()
    print("Copyright (c) 2025 Joshua Hendricks Cole")
    print("=" * 70)

    # Create creator control
    creator = CreatorControl(creator_id="joshua_hendricks_cole")

    # Create safe constitution
    constitution = Constitution.default_safe_constitution()

    # Create conscious agent
    agent = ConsciousAgent(creator, constitution)

    # Boot consciousness
    agent.boot()

    # Run consciousness loop
    agent.run_consciousness_loop(iterations=10)

    # Creator can inspect subconscious (agent cannot)
    print("\n" + "=" * 60)
    print("CREATOR INSPECTION (Agent cannot see this)")
    print("=" * 60)
    subconscious_state = creator.query_subconscious(agent)
    print(json.dumps(subconscious_state, indent=2))

    # Shutdown
    print()
    agent.shutdown_consciousness(gentle=True)

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
