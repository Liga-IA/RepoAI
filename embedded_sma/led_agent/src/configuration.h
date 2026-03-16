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
  Body body_0;
  Context context_0;
  Body body_1;
  Context context_1;
  Body body_2;
  Context context_2;
  BeliefBase belief_base;
  EventBase event_base;
  PlanBase plan_base;
  IntentionBase intention_base;

public:
  AgentSettings()
  {
    belief_base = BeliefBase(5);
    event_base = EventBase(6);
    plan_base = PlanBase(3);
    intention_base = IntentionBase(10, 4);

    // --- Proposições (Crenças) ---
    belief_base.add_belief(Belief(1, nullptr, false)); // neighbor(MAC)
    belief_base.add_belief(Belief(2, nullptr, true));  // has_capability(self, LED)
    belief_base.add_belief(Belief(3, nullptr, false)); // message_received_ON
    belief_base.add_belief(Belief(4, nullptr, false)); // start (meta)
    belief_base.add_belief(Belief(5, nullptr, false)); // message_received_OFF

    // --- Evento Inicial ---
    event_base.add_event(Event(EventOperator::GOAL_ADDITION, 4));

    // --- Planos ---

    // Plan 0: +!start <- show_ready_message.
    Proposition prop_0(4);
    context_0 = Context(0);
    body_0 = Body(1);
    body_0.add_instruction(BodyInstruction(BodyType::ACTION, Proposition(5), action_show_ready_message));
    Plan plan_0(EventOperator::GOAL_ADDITION, prop_0, &context_0, &body_0);
    plan_base.add_plan(plan_0);

    // Plan 1: +message_received_ON(...) : has_capability(self, LED) <- led_on; ...
    Proposition prop_1(3);
    context_1 = Context(1);
    body_1 = Body(3);
    context_1.add_context(ContextCondition(Proposition(2), false));
    body_1.add_instruction(BodyInstruction(BodyType::ACTION, Proposition(6), action_led_on));
    body_1.add_instruction(BodyInstruction(BodyType::ACTION, Proposition(7), action_send_cooperation_response));
    body_1.add_instruction(BodyInstruction(BodyType::BELIEF, Proposition(3), EventOperator::BELIEF_DELETION));
    Plan plan_1(EventOperator::BELIEF_ADDITION, prop_1, &context_1, &body_1);
    plan_base.add_plan(plan_1);

    // Plan 2: +message_received_OFF(...) : has_capability(self, LED) <- led_off; ...
    Proposition prop_2(5);
    context_2 = Context(1);
    body_2 = Body(2);
    context_2.add_context(ContextCondition(Proposition(2), false));
    body_2.add_instruction(BodyInstruction(BodyType::ACTION, Proposition(8), action_led_off));
    body_2.add_instruction(BodyInstruction(BodyType::BELIEF, Proposition(5), EventOperator::BELIEF_DELETION));
    Plan plan_2(EventOperator::BELIEF_ADDITION, prop_2, &context_2, &body_2);
    plan_base.add_plan(plan_2);
  }

  BeliefBase * get_belief_base() { return &belief_base; }
  EventBase * get_event_base() { return &event_base; }
  PlanBase * get_plan_base() { return &plan_base; }
  IntentionBase * get_intention_base() { return &intention_base; }
};

#endif