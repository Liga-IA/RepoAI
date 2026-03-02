/*
 * test_data.h
 *
 *  Created on: Jul 25, 2020
 *      Author: Matuzalem Muller
 */

#ifndef COMMON_TEST_FUNCTIONS_H_
#define COMMON_TEST_FUNCTIONS_H_

static int shared_var;

inline bool action_do_nothing()
{
  return true;
}

inline bool action_say_hello()
{
  return true;
}

inline bool return_true_beliefbase()
{
  return true;
}

inline bool return_false_beliefbase()
{
  return false;
}

inline bool return_true_bool(bool var)
{
  return true;
}

inline bool return_false_bool(bool var)
{
  return false;
}

inline bool update_belief_1_revert_state(bool var)
{
  return !var;
}

inline bool update_belief_2_revert_state(bool var)
{
  return !var;
}

inline bool update_belief_3_revert_state(bool var)
{
  return !var;
}

inline bool update_belief_4_revert_state(bool var)
{
  return !var;
}

inline bool update_belief_5_revert_state(bool var)
{
  return !var;
}

inline bool update_belief_6_revert_state(bool var)
{
  return !var;
}

inline bool update_belief_7_revert_state(bool var)
{
  return !var;
}

inline bool update_belief_8_revert_state(bool var)
{
  return !var;
}

inline bool update_happy(bool var)
{
  return !var;
}

inline bool update_i_am_host(bool var)
{
  return !var;
}

#endif
