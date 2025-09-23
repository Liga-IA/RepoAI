/*
 * plan.h
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#ifndef BDI_PLAN_H_
#define BDI_PLAN_H_

#include "event_base.h"
#include "body.h"
#include "context.h"
#include <cstdint>

/**
 * Represents agent plan.
 */
class Plan
{
private:
  EventOperator _operator;
  Proposition _proposition;
  Context * _context;
  Body * _body;

public:
  /**
   * Plan constructor
   * @param op Triggering EventOperator
   * @param prop Triggering Event Proposition/name
   * @param context Context
   * @param body Body with instructions
   */
  Plan(EventOperator op, Proposition prop, Context * context, Body * body);

  /**
   * Run instruction from Plan Body at specific index
   * @param index Position in Body of BodyInstruction to be executed
   * @param beliefs Agent's BeliefBase
   * @param events Agent's EventBase
   */
  BodyReturn run_body(std::uint8_t index,
                      BeliefBase * beliefs,
                      EventBase * events);

  const EventOperator & get_operator() const
  {
    return _operator;
  }

  Proposition * get_proposition()
  {
     return &_proposition;
  }

  Context * get_context()
  {
     return _context;
  }

  Body * get_body()
  {
     return _body;
  }
};

#endif /* BDI_PLAN_H_ */
