/*
 * body.h
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#ifndef SYNTAX_BODY_H_
#define SYNTAX_BODY_H_

#include "body_instruction.h"
#include "belief_base.h"
#include "event_base.h"
#include "vector_queue.h"
#include <cstdint>

/**
 * Represents plan body with collection of body instructions.
 */
class Body
{
  /// Vector of BodyInstructions
  VectorQueue<BodyInstruction> _body;
  /// Max size of _body vector
  std::uint8_t _size = 0;

public:
  Body();

  /**
   * Body constructor
   * @param size Size of _body
   */
  Body(std::uint8_t size);

  /**
   * Run instruction from Body at specific position
   * @param index Position in Body of instruction to be run
   * @param beliefs Agent's BeliefBase
   * @param events Agent's EventBase
   */
  BodyReturn run_body(std::uint8_t index,
                      BeliefBase * beliefs,
                      EventBase * events);

  /**
   * Adds instruction to Body
   * @param instruction BodyInstruction to add to _body vector
   */
  bool add_instruction(BodyInstruction instruction);

  std::uint8_t get_size();
};

#endif /* SYNTAX_BODY_H_ */
