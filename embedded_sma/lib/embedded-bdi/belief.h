/*
 * belief.h
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#ifndef BDI_BELIEF_H_
#define BDI_BELIEF_H_

#include "proposition.h"
#include <cstdint>

/**
 * Represents the belief of an agent which can be true or false.
 * Beliefs also contain an update function so the values can be automatically
 * updated by the agent.
 */
class Belief
{
private:
  Proposition _proposition;
  /// State of Belief
  bool _belief_state = false;
  ///@{ Function to update _belief_state.
  /// var receives the current value of _belief_state
  ///@}
  bool (*_update)(bool var) = nullptr;

public:
  /**
   * Belief constructor
   * @param prop Belief Proposition
   * @param update_function Function to update _belief_state
   * @param belief_state Belief state. Default is false
   */
  Belief(Proposition prop,
         bool (*update_function)(bool var),
         bool belief_state = false);

  /**
   * Update _belief_state based on _update function
   * @return true if _belief_state is changed, false otherwise
   */
  bool update_belief();

  /**
   * Update _belief_state
   * @param state Value to be assigned to _belief_state
   */
  void change_state(bool state);

  const Proposition & get_proposition() const
  {
    return _proposition;
  }

  bool & get_state()
  {
    return _belief_state;
  }
};

#endif /* CLASSES_BELIEF_H_ */
