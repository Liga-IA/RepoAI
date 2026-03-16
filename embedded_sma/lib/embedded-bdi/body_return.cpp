/*
 * body_return.cpp
 *
 *  Created on: Jul 17, 2020
 *      Author: Matuzalem Muller
 */

#include "body_return.h"

BodyReturn::BodyReturn()
{
  _type = BodyType::ACTION;
  _value = false;
  _event = nullptr;
}

BodyReturn::BodyReturn(BodyType type, bool value, EventID * event)
{
  _type = type;
  _value = value;
  _event = event;
}
