/*
 * context_condition.h
 *
 *  Created on: Jul 16, 2020
 *      Author: Matuzalem Muller
 */

#ifndef SYNTAX_CONTEXT_CONDITION_H_
#define SYNTAX_CONTEXT_CONDITION_H_

#include "proposition.h"
#include <cstdint>

/**
 * Represents a literal from the plan's context.
 */
class ContextCondition
{
private:
  Proposition _proposition;
  bool _is_negated;

public:
  /**
   * ContextCondition constructor
   * @param prop Proposition to be compared with belief from BeliefBase
   * @param is_negated Indicates if the context is positive or negative
   */
  ContextCondition(Proposition prop, bool is_negated = false);

  const Proposition & get_proposition() const
  {
    return _proposition;
  }

  bool is_negated() const
  {
    return _is_negated;
  }
};

#endif /* SYNTAX_CONTEXT_CONDITION_H_ */
