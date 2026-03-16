/*
 * proposition.cpp
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#include "proposition.h"

Proposition::Proposition() {
  _name = 0;
}

Proposition::Proposition(std::uint8_t name)
{
  _name = name;
}

bool Proposition::is_equal(Proposition * prop) const
{
  return (_name == prop->get_name());
}

bool Proposition::is_equal(Proposition prop) const
{
  return (_name == prop.get_name());
}
