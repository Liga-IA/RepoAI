/*
 * body.cpp
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#include "body.h"

Body::Body()
{
  _size = 0;
}

Body::Body(std::uint8_t size)
{
  _size = size;
  _body.init(size);
}

BodyReturn Body::run_body(std::uint8_t index,
                          BeliefBase * beliefs,
                          EventBase * events)
{
  BodyReturn result;

  if (index >= _body.size())
  {
    result = BodyReturn(BodyType::ACTION, false, nullptr);
  }
  else
  {
//    std::uint8_t reverse_index = _body.size() - index - 1;
//    result = _body.item_at(reverse_index)->run_instruction(beliefs, events);
    result = _body.item_at(index)->run_instruction(beliefs, events);
  }

  return result;
}

bool Body::add_instruction(BodyInstruction instruction)
{
  if (_body.size() == _size)
  {
    return false;
  }

//  _body.push_front(instruction);
  _body.push_back(instruction);

  return true;
}

std::uint8_t Body::get_size()
{
  return _body.size();
}
