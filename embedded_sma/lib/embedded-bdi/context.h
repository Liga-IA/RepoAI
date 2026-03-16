/*
 * context.h
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#ifndef SYNTAX_CONTEXT_H_
#define SYNTAX_CONTEXT_H_

#include "context_condition.h"
#include "belief_base.h"
#include "vector_queue.h"
#include <cstdint>

/**
 * Represents the context of a plan.
 */
class Context
{
  /// Vector of ContextConditions
  VectorQueue <ContextCondition> _context;
  /// Max size of _context vector
  std::uint8_t _size = 0;

public:
  Context();

  /**
   * Context constructor
   * @param size Max size of context queue
   */
  Context(std::uint8_t size);

  /**
   * Adds belief to _context buffer
   * @param value ContextCondition to be added
   * @return true if value is added to buffer, false otherwise
   */
  bool add_context(ContextCondition value);

  /**
   * Checks if context is valid
   * @param beliefs Checks if propositions from vector of ContextConditions have
   * the expected values given the BeliefBase
   */
  bool is_valid (BeliefBase * beliefs);
};

#endif /* SYNTAX_CONTEXT_H_ */
