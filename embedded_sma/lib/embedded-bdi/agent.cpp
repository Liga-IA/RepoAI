/*
 * agent.cpp
 *
 *  Created on: Sep 10, 2020
 *      Author: Matuzalem Muller
 */

#include "agent.h"

Agent::Agent(BeliefBase * beliefs,
             EventBase * events,
             PlanBase * plans,
             IntentionBase * intentions)
{
  this->beliefs = beliefs;
  this->events = events;
  this->plans = plans;
  this->intentions = intentions;
  this->plan_to_act = nullptr;
}

void Agent::run()
{
  // The original beliefs->update(events) is not used for this agent architecture.

  // Checks if there are events to be processed
  if (!events->is_empty())
  {
    event_to_process = events->get_event();

    // Before looking for a plan, update the belief base if the event is a belief change.
    if (event_to_process.get_operator() == EventOperator::BELIEF_ADDITION)
    {
        beliefs->change_belief_state(event_to_process.get_proposition(), true);
    }
    else if (event_to_process.get_operator() == EventOperator::BELIEF_DELETION)
    {
        beliefs->change_belief_state(event_to_process.get_proposition(), false);
    }

    // Now, with the belief base correctly updated, find a relevant plan for the SAME event.
    plan_to_act = plans->revise(&event_to_process, beliefs);
    if (plan_to_act) {
      intentions->add_intention(plan_to_act, &event_to_process);
    }
  }

  // Runs intention in case there are any
  if (!intentions->is_empty())
  {
    intentions->run_intention_base(beliefs, events, plans);
  }
}