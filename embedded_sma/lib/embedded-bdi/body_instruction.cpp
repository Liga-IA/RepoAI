/*
 * body_instruction.cpp
 *
 *  Created on: Jul 24, 2020
 *      Author: Matuzalem Muller
 */

#include "body_instruction.h"

BodyInstruction::BodyInstruction(BodyType type,
                                 Proposition prop,
                                 bool (*take_action)())
{
  _type = type;
  _proposition = prop;
  _take_action = take_action;
  _operator = EventOperator::BELIEF_ADDITION;
}

BodyInstruction::BodyInstruction(BodyType type,
                                 Proposition prop,
                                 EventOperator event_operator)
{
  _type = type;
  _proposition = prop;
  _take_action = nullptr;
  _operator = event_operator;
}

// Add handling of belief that is not in beliefbase
BodyReturn BodyInstruction::run_instruction(BeliefBase * belief_base,
                                            EventBase * event_base)
{
  BodyReturn result;
  Event event(_operator, _proposition);

  if (_type == BodyType::ACTION)
  {
    bool value = _take_action();
    result = BodyReturn(BodyType::ACTION, value, nullptr);
  }
  else if (_type == BodyType::BELIEF)
  {
    if (event_base->add_event(event))
    {
      if (_operator == EventOperator::BELIEF_ADDITION)
      {
        belief_base->change_belief_state(_proposition, true);
      }
      else
      {
        belief_base->change_belief_state(_proposition, false);
      }
      result = BodyReturn(BodyType::BELIEF,
                          true,
                          event_base->last_event()->get_event_id()
                          );
    }
    else
    {
      result = BodyReturn(BodyType::BELIEF, false, nullptr);
    }
  }
  else
  {
    if (event.get_operator() == EventOperator::GOAL_ACHIEVE)
    {
      event_base->add_event(event);
      result = BodyReturn(
                          BodyType::GOAL,
                          true,
                          nullptr
                          );
    }
    else if (event_base->add_event(event))
    {
      result = BodyReturn(
                          BodyType::GOAL,
                          true,
                          event_base->last_event()->get_event_id()
                          );
    }
    else
    {
      result = BodyReturn(BodyType::GOAL, false, nullptr);
    }
  }

  return result;
}
