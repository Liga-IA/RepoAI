/*
 * belief_base.h
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#ifndef BDI_BELIEF_BASE_H_
#define BDI_BELIEF_BASE_H_

#include "belief.h"
#include "event.h"
#include "event_base.h"
#include "vector_queue.h"
#include <cstdint>

/**
 * Collection of agent beliefs.
 */
class BeliefBase
{
private:
  /// Vector of Beliefs
  VectorQueue<Belief> _belief_base;
  /// Max size of _belief_base vector
  std::uint8_t _size = 0;

public:
  BeliefBase();

  /**
   * BeliefBase's constructor
   * @param size Size of _belief_base buffer
   */
  BeliefBase(std::uint8_t size);

  /**
   * Adds belief to _belief_base. Does not avoid/check for duplicates
   * @param belief Belief to be added
   * @return true is belief is added, false otherwise
   */
  bool add_belief(Belief belief);

  /**
   * Updates belief _belief_state based on belief's _update function
   * @param event_base Agent's EventBase. An event is added to the EventBase in
   * case _belief_state changes (true->false, false->true)
   */
  void update(EventBase * event_base);

  /**
   * Change the _belief_state of a belief
   * @param prop Belief's proposition
   * @param state New _belief_state value
   * @return false if Belief does not exist, true otherwise
   */
  bool change_belief_state(Proposition prop, bool state);

  /**
   * Get _belief_state value of belief that matches given proposition
   * @param prop Proposition to match belief's proposition
   * @return belief's value. False if belief does not exist in BeliefBase
   */
  bool get_belief_state(Proposition prop);

  /**
   * Size of BeliefBase
   * @return Size of _belief_base
   */
  const std::uint8_t get_size();
};

#endif /* CLASSES_BELIEFBASE_H_ */
