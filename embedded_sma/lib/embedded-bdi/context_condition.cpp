/*
 * context_condition.cpp
 *
 *  Created on: Jul 16, 2020
 *      Author: Matuzalem Muller
 */

#include "context_condition.h"

ContextCondition::ContextCondition(Proposition prop, bool is_negated)
{
  _proposition = prop;
  _is_negated = is_negated;
}
