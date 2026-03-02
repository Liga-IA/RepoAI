/*
 * event_operator.h
 *
 *  Created on: Jul 5, 2020
 *      Author: Matuzalem Muller
 */

#ifndef SYNTAX_EVENT_OPERATOR_H_
#define SYNTAX_EVENT_OPERATOR_H_

/**
 * Event types:
 *   * BELIEF_ADDITION (+): Addition of belief to belief base
 *   * BELIEF_DELETION (-): Deletion of belief from belief base
 *   * GOAL_ADDITION (+!): Addition of (sub)goal
 *   * GOAL_DELETION (-!): Deletion of (sub)goal
 *   * GOAL_ACHIEVE (!!): Non-blocking addition of subgoal
 *   * TEST_GOAL_ADDITION (+?!): Addition of test (sub)goal
 *   * TEST_GOAL_DELETION (+?-): Deletion of test (sub)goal
 */
enum class EventOperator : unsigned char
{
  BELIEF_ADDITION,      // +
  BELIEF_DELETION,      // -
  GOAL_ADDITION,        // +!
  GOAL_DELETION,        // -!
  GOAL_ACHIEVE,         // !!
  TEST_GOAL_ADDITION,   // +?!
  TEST_GOAL_DELETION,   // -?!
};

#endif /* SYNTAX_EVENT_OPERATOR_H_ */
