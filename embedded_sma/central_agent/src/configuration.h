#ifndef CONFIGURATION_H_
#define CONFIGURATION_H_

#include "belief_base.h"
#include "event_base.h"
#include "plan_base.h"
#include "intention_base.h"
#include "functions.h"

class AgentSettings
{
private:
  Body body_0, body_1, body_2, body_3, body_4, body_5, body_6, body_7;
  Context context_0, context_1, context_2, context_3, context_4, context_5, context_6, context_7;
  BeliefBase belief_base;
  EventBase event_base;
  PlanBase plan_base;
  IntentionBase intention_base;

public:
  AgentSettings()
  {
    belief_base = BeliefBase(16);
    event_base = EventBase(10);
    plan_base = PlanBase(8); // More plans
    intention_base = IntentionBase(12, 5);

    // --- Propositions (Beliefs) ---
    belief_base.add_belief(Belief(0, nullptr, false)); // low_light
    belief_base.add_belief(Belief(1, nullptr, false)); // alarm_request_received
    belief_base.add_belief(Belief(2, nullptr, false)); // neighbor_with_led
    belief_base.add_belief(Belief(3, nullptr, false)); // has_capability(neighbor, LED)
    belief_base.add_belief(Belief(4, nullptr, true));  // has_capability(self, BUZZER)
    belief_base.add_belief(Belief(5, nullptr, false)); // is_hot
    belief_base.add_belief(Belief(6, nullptr, false)); // is_humid
    belief_base.add_belief(Belief(8, nullptr, false)); // pot_is_high
    belief_base.add_belief(Belief(9, nullptr, false)); // cooling_active
    belief_base.add_belief(Belief(10, nullptr, true)); // start (goal)
    belief_base.add_belief(Belief(12, nullptr, false)); // cool_down_room (goal)

    // --- Initial Event ---
    event_base.add_event(Event(EventOperator::GOAL_ADDITION, 10));

    // --- Plans ---

    // Plan 0: +!start <- show_ready_message.
    Proposition prop_0(10);
    context_0 = Context(0);
    body_0 = Body(1);
    body_0.add_instruction(BodyInstruction(BodyType::ACTION, Proposition(100), action_show_ready_message));
    plan_base.add_plan(Plan(EventOperator::GOAL_ADDITION, prop_0, &context_0, &body_0));

    // Plan 1: +low_light : neighbor_with_led & has_capability(LED) <- request_cooperation_on.
    Proposition prop_1(0);
    context_1 = Context(2);
    body_1 = Body(1);
    context_1.add_context(ContextCondition(Proposition(2), false));
    context_1.add_context(ContextCondition(Proposition(3), false));
    body_1.add_instruction(BodyInstruction(BodyType::ACTION, Proposition(101), action_request_cooperation_on));
    plan_base.add_plan(Plan(EventOperator::BELIEF_ADDITION, prop_1, &context_1, &body_1));

    // Plan 2: -low_light : neighbor_with_led & has_capability(LED) <- request_cooperation_off.
    Proposition prop_2(0);
    context_2 = Context(2);
    body_2 = Body(1);
    context_2.add_context(ContextCondition(Proposition(2), false));
    context_2.add_context(ContextCondition(Proposition(3), false));
    body_2.add_instruction(BodyInstruction(BodyType::ACTION, Proposition(102), action_request_cooperation_off));
    plan_base.add_plan(Plan(EventOperator::BELIEF_DELETION, prop_2, &context_2, &body_2));

    // Plan 3: +alarm_request_received : has_capability(BUZZER) <- sound_buzzer.
    Proposition prop_3(1);
    context_3 = Context(1);
    body_3 = Body(2);
    context_3.add_context(ContextCondition(Proposition(4), false));
    body_3.add_instruction(BodyInstruction(BodyType::ACTION, Proposition(103), action_sound_buzzer));
    body_3.add_instruction(BodyInstruction(BodyType::BELIEF, Proposition(1), EventOperator::BELIEF_DELETION));
    plan_base.add_plan(Plan(EventOperator::BELIEF_ADDITION, prop_3, &context_3, &body_3));

    // --- New Plans for Temperature Control ---

    // Plan 4: +is_hot : not cooling_active <- +cooling_active, +!cool_down_room.
    Proposition prop_4(5); // Trigger: is_hot
    context_4 = Context(1);
    context_4.add_context(ContextCondition(Proposition(9), true)); // Context: not cooling_active
    body_4 = Body(2);
    body_4.add_instruction(BodyInstruction(BodyType::BELIEF, Proposition(9), EventOperator::BELIEF_ADDITION));
    body_4.add_instruction(BodyInstruction(BodyType::GOAL, Proposition(12), EventOperator::GOAL_ADDITION));
    plan_base.add_plan(Plan(EventOperator::BELIEF_ADDITION, prop_4, &context_4, &body_4));

    // Plan 5: +!cool_down_room : not pot_is_high <- sound_buzzer, +!cool_down_room.
    Proposition prop_5(12); // Trigger: cool_down_room goal
    context_5 = Context(1);
    context_5.add_context(ContextCondition(Proposition(8), true)); // Context: not pot_is_high
    body_5 = Body(2);
    body_5.add_instruction(BodyInstruction(BodyType::ACTION, Proposition(104), action_sound_buzzer));
    body_5.add_instruction(BodyInstruction(BodyType::GOAL, Proposition(12), EventOperator::GOAL_ADDITION)); // Re-post goal to loop
    plan_base.add_plan(Plan(EventOperator::GOAL_ADDITION, prop_5, &context_5, &body_5));

    // Plan 6: +!cool_down_room : pot_is_high <- -cooling_active.
    Proposition prop_6(12); // Trigger: cool_down_room goal
    context_6 = Context(1);
    context_6.add_context(ContextCondition(Proposition(8), false)); // Context: pot_is_high
    body_6 = Body(1);
    body_6.add_instruction(BodyInstruction(BodyType::BELIEF, Proposition(9), EventOperator::BELIEF_DELETION)); // Goal is achieved, stop cooling
    plan_base.add_plan(Plan(EventOperator::GOAL_ADDITION, prop_6, &context_6, &body_6));

    // Plan 7: -is_hot : cooling_active <- -cooling_active, -!cool_down_room.
    Proposition prop_7(5); // Trigger: no longer hot
    context_7 = Context(1);
    context_7.add_context(ContextCondition(Proposition(9), false)); // Context: cooling_active
    body_7 = Body(2);
    body_7.add_instruction(BodyInstruction(BodyType::BELIEF, Proposition(9), EventOperator::BELIEF_DELETION));
    body_7.add_instruction(BodyInstruction(BodyType::GOAL, Proposition(12), EventOperator::GOAL_DELETION));
    plan_base.add_plan(Plan(EventOperator::BELIEF_DELETION, prop_7, &context_7, &body_7));
  }

  BeliefBase * get_belief_base() { return &belief_base; }
  EventBase * get_event_base() { return &event_base; }
  PlanBase * get_plan_base() { return &plan_base; }
  IntentionBase * get_intention_base() { return &intention_base; }
};

#endif