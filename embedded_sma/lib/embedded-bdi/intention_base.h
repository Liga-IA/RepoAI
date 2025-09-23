/*
 * intention_base.h
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#ifndef BDI_INTENTION_BASE_H_
#define BDI_INTENTION_BASE_H_

#include "belief_base.h"
#include "event_base.h"
#include "intention.h"
#include "plan.h"
#include "vector_queue.h"
#include <cstdint>

/**
 * Collection of agent intentions.
 */
class IntentionBase
{
private:
  /// Vector of Intentions
  VectorQueue<Intention> _intention_base;
  /// Max size of _intention_base vector
  std::uint8_t _buffer_size = 0;
  /// Max size of each Intention _plans stack vector
  std::uint8_t _stack_size = 0;

  /**
   * Stacks plan to existing intention
   * @param plan Plan to be added in Intention stack
   * @param event Event that generated the Event
   * @return true if Plan is stacked, false otherwise
   */
  bool stack_plan(Plan * plan, Event * event);

public:
  IntentionBase();

  /**
   * IntentionBase constructor
   * @param buffer_size Size of the buffer where the intentions are stored
   * @param stack_size Size of each Intention stack
   */
  IntentionBase(std::uint8_t buffer_size, std::uint8_t stack_size);

  /**
   * Creates new Intention with given Plan or adds Plan to existing Intention
   * stack
   * @param plan Pointer to Plan to be instantiated as Intention
   * @param event Event that generated Plan
   */
  void add_intention(Plan * plan, Event * event);

  /**
   * Run instruction from the front of _intention_base
   * If Intention is suspended and blocking Event was not yet processed, place
   * Intention in the back of the queue. If Event was processed and Intention
   * is still suspended, remove it from _intention_base
   * After instruction is run, the Intention is placed at the end of
   * _intention_base if it has not finished
   */
  void run_intention_base(BeliefBase * beliefs,
                          EventBase * events,
                          PlanBase * plans);

  /**
   * Returns if IntentionBase is empty based on _intention_base size
   * @return True if empty, false otherwise
   */
  bool is_empty();

  /**
   * Returns if IntentionBase is full based on _intention_base size
   * @return True if full, false otherwise
   */
  bool is_full();
};

#endif /* BDI_INTENTION_BASE_H_ */
