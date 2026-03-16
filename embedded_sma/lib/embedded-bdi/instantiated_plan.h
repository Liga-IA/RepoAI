/*
 * instantiated_plan.h
 *
 *  Created on: Jul 12, 2020
 *      Author: Matuzalem Muller
 */

#ifndef BDI_INSTANTIATED_PLAN_H_
#define BDI_INSTANTIATED_PLAN_H_

#include "plan.h"
#include <cstdint>

/**
 * Instantiates plan so it can be run.
 */
class InstantiatedPlan
{
private:
  /// Pointer to plan to be run
  Plan * _plan;
  /// Index of Plan instruction list
  std::uint8_t _index = 0;

public:
  /**
   * InstantiatedPlan constructor
   * @param plan Pointer to Plan
   */
  InstantiatedPlan(Plan * plan);

  /**
   * Run instruction from position _index from Plan _plan
   * @param beliefs Agent BeliefBase
   * @param events Agent EventBase
   * @return BodyReturn that lists BodyType, _value and EventID
   * of generated event (if any)
   */
  BodyReturn run_plan(BeliefBase * beliefs, EventBase * events);

  /**
   * Returns if the entire Plan from _plan has been run
   * @return True if all instructions from _plan were run, false otherwise
   */
  bool is_finished();

  Plan * get_plan()
  {
    return _plan;
  }
};

#endif /* BDI_INSTANTIATED_PLAN_H_ */
