/*
 * intention.h
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#ifndef BDI_INTENTION_H_
#define BDI_INTENTION_H_

#include "plan_base.h"
#include "belief_base.h"
#include "instantiated_plan.h"
#include "vector_queue.h"
#include <cstdint>

/**
 * Represents agent intention with stack of plans to be run.
 */
class Intention
{
private:
  /// Vector of InstantiatedPlan that represents Intention stack
  VectorQueue<InstantiatedPlan> _plans;
  /// Max size of _plans stack
  std::uint8_t _size;
  /// Identified of Event that suspends intention from running
  EventID * _suspended_by;
  bool suspended_by_belief_event;

  /**
   * Suspend intention. Intentions should be suspended when the instruction
   * ran on run_intention is added to the EventBase and no further instructions
   * can be run without processing the event first
   * @param event_id Pointer to EventID that blocks the intention from running
   */
  void suspend(EventID * event_id, EventBase * events);



public:
  /**
   * Intention constructor
   * @param plan Pointer to plan to be instantiated as intention
   * @param size Size of _plans stack
   */
  Intention(Plan * plan, std::uint8_t size);

  /**
   * Stack plan in _plan stack
   * @param plan Plan to be stacked
   * @return true if plan is added, false otherwise. False means that size of
   * _plans stack was exceeded and intention should likely be dropped
   */
  bool stack_plan(Plan * plan);

  /**
   * Run one instruction from plan from the top of _plans stack
   * @param beliefs Agent's BeliefBase
   * @param events Agent's EventBase
   * @return
   */
  bool run_intention(BeliefBase * beliefs, EventBase * events);

  /**
   * Check if intention is suspended by given event
   * @param event EventBase
   * @return true if Intention is suspended and _suspended_by still exists
   * in EventBase, false otherwise
   */
  bool is_suspended_by(Event * event);

  /**
   * Checks if intention execution finished based on size of _plans
   * @return true if intention is finished, false otherwise
   */
  bool is_finished();

  /**
   * Handles termination by adding goal deletion events to EventBase
   * @param beliefs Agent BeliefBase
   * @param events Agent EventBase where events will be added
   * @param plans Agent PlanBase where fail plans will be searched
   */
  void terminate(BeliefBase * beliefs, EventBase * events, PlanBase * plans);

  /**
   * Checks if event is suspended
   * @return true if suspended, false otherwise
   */
  bool is_suspended();

  bool is_suspended_by_belief_event();

  EventID * get_event_id()
  {
    return _suspended_by;
  }

  /**
   * Unsuspend intention so instructions can be run
   */
  void unsuspend();
};

#endif /* BDI_INTENTION_H_ */
