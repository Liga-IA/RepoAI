/*
 * belief.cpp
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#include "belief.h"

Belief::Belief(Proposition prop,
               bool (*update_function)(bool var),
               bool belief_state)
{
  _proposition = prop;
  _belief_state = belief_state;
  _update = update_function;
}

bool Belief::update_belief()
{
  if (_update)
  {
    bool current_value = _belief_state;
    _belief_state = _update(_belief_state);
    if (_belief_state != current_value)
    {
      return true;
    }
    else
    {
      return false;
    }
  }

  return false;
}

void Belief::change_state(bool state)
{
  _belief_state = state;
}
