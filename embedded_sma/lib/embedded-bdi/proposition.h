/*
 * proposition.h
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#ifndef SYNTAX_PROPOSITION_H_
#define SYNTAX_PROPOSITION_H_

#include <cstdint>

/**
 * Represents logical proposition.
 */
class Proposition
{
private:
  /// Proposition name
  std::uint8_t _name;

public:
  Proposition();

  Proposition(std::uint8_t name);

  /**
   * Compares value of current proposition with given proposition.
   * @param prop Proposition to be compared
   * @return true if equal, false otherwise
   */
  bool is_equal(Proposition prop) const;

  /**
   * Compares value of current proposition with given proposition.
   * @param prop Pointer to proposition to be compared
   * @return true if equal, false otherwise
   */
  bool is_equal(Proposition * prop) const;

  const std::uint8_t & get_name() const
  {
    return _name;
  }
};

#endif /* SYNTAX_PROPOSITION_H_ */
