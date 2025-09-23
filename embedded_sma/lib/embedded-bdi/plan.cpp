/*
 * plan.cpp
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#include "plan.h"

Plan::Plan(EventOperator op, Proposition prop, Context * context, Body * body)
{
  _operator = op;
  _proposition = prop;
  _context = context;
  _body = body;
}

BodyReturn Plan::run_body(std::uint8_t index,
                          BeliefBase * beliefs,
                          EventBase * events)
{
  return _body->run_body(index, beliefs, events);
}