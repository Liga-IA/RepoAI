/*
 * intention_base.cpp
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#include "intention_base.h"

IntentionBase::IntentionBase()
{
  _buffer_size = 0;
  _stack_size = 0;
}

IntentionBase::IntentionBase(std::uint8_t buffer_size, std::uint8_t stack_size)
{
  _buffer_size = buffer_size;
  _stack_size = stack_size;
  _intention_base.init(buffer_size);
}

void IntentionBase::add_intention(Plan * plan, Event * event)
{
  if (plan == nullptr)
  {
    return;
  }

  if(this->stack_plan(plan, event))
  {
    return;
  }

  if (this->is_full())
  {
    return;
  }

  Intention intention(plan, _stack_size);
  _intention_base.push_front(intention);
}

bool IntentionBase::stack_plan(Plan * plan, Event * event)
{
  for (std::uint8_t i = 0; i < _intention_base.size(); i++)
  {
    if (_intention_base.item_at(i)->is_suspended_by(event))
    {
      if (!_intention_base.item_at(i)->stack_plan(plan))
      {
        _intention_base.erase(i);
      }
      return true;
    }
  }

  return false;
}

void IntentionBase::run_intention_base(BeliefBase * beliefs,
                                       EventBase * events,
                                       PlanBase * plans)
{
  if (_intention_base.size() == 0)
  {
    return;
  }

  if (_intention_base.back()->is_suspended())
  {
    if (events->event_exists(_intention_base.back()->get_event_id()))
    {
      _intention_base.rotate();
    }
    else if (_intention_base.back()->is_suspended_by_belief_event())
    {
      _intention_base.back()->unsuspend();
    }
    else
    {
      _intention_base.back()->terminate(beliefs, events, plans);
      _intention_base.pop_back();
    }
    return;
  }

  // Runs plan
  if (_intention_base.size() == 0)
  {
    return;
  }

  if (!_intention_base.back()->run_intention(beliefs, events))
  {
    _intention_base.back()->terminate(beliefs, events, plans);
    _intention_base.pop_back();
  }
  else
  {
    if (_intention_base.back()->is_finished())
    {
      _intention_base.pop_back();
    }
    else
    {
      _intention_base.rotate();
    }
  }
}

bool IntentionBase::is_empty() {
  return (_intention_base.size() == 0);
}

bool IntentionBase::is_full() {
  return (_intention_base.size() == _buffer_size);
}
