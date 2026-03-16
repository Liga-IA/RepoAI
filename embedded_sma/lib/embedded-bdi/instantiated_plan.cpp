/*
 * instantiated_plan.cpp
 *
 *  Created on: Jul 12, 2020
 *      Author: Matuzalem Muller
 */

#include "instantiated_plan.h"

InstantiatedPlan::InstantiatedPlan(Plan * plan)
{
  _plan = plan;
}

BodyReturn InstantiatedPlan::run_plan(BeliefBase * beliefs, EventBase * events)
{
  BodyReturn result;

  if (_index < _plan->get_body()->get_size())
  {
    result = _plan->run_body(_index, beliefs, events);
    _index++;
  }
  else
  {
    result = BodyReturn(BodyType::ACTION, false, nullptr);
  }

  return result;
}

bool InstantiatedPlan::is_finished()
{
  return (_index == _plan->get_body()->get_size());
}
