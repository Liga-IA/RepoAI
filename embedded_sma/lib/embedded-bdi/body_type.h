/*
 * body_type.h
 *
 *  Created on: Jul 5, 2020
 *      Author: Matuzalem Muller
 */

#ifndef SYNTAX_BODY_BODY_TYPE_H_
#define SYNTAX_BODY_BODY_TYPE_H_

/**
 * Represents type of body instructions: Action, Goal or Belief operation.
 */
enum class BodyType : unsigned char
{
  ACTION,
  GOAL,
  BELIEF
};

#endif /* SYNTAX_BODY_BODY_TYPE_H_ */
