/*
 * intention.cpp
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#include "intention.h"


Intention::Intention(Plan * plan, std::uint8_t size)
{
  _size = size;
  _suspended_by = nullptr;
  suspended_by_belief_event = false;
  _plans.init(size);
  InstantiatedPlan inst_plan(plan);
  _plans.push_back(inst_plan);
}

bool Intention::stack_plan(Plan * plan)
{
  if (!plan || (_plans.size() == _size))
  {
    return false;
  }

  InstantiatedPlan inst_plan(plan);
  _plans.push_back(plan);

  this->unsuspend();

  return true;
}

bool Intention::run_intention(BeliefBase * beliefs, EventBase * events)
{
  if (_plans.size() == 0 || this->is_suspended())
  {
    return false;
  }

  BodyReturn value = _plans.back()->run_plan(beliefs, events);

  // If instruction execution fails, return false
  if (value.get_value())
  {
    if (value.get_event())
    {
      this->suspend(value.get_event(), events);
    }
    else
    {
      while (_plans.size() > 0)
      {
        if (_plans.back()->is_finished()){
          _plans.pop_back();
        }
        else
        {
          break;
        }
      }
    }
  }

  return value.get_value();
}

void Intention::suspend(EventID * event_id, EventBase * events)
{
  _suspended_by = event_id;

  Event * event = events->get_event_by_id(event_id);
  if (event)
  {
    if (event->get_operator() == EventOperator::BELIEF_ADDITION ||
    	event->get_operator() == EventOperator::BELIEF_DELETION)
    {
      this->suspended_by_belief_event = true;
    }
  }
}

void Intention::unsuspend()
{
  _suspended_by = nullptr;
  this->suspended_by_belief_event = false;
}

bool Intention::is_suspended_by(Event * event)
{
  if ((_suspended_by == nullptr) || !event)
  {
    return false;
  }
  else
  {
    if (this->_suspended_by->is_equal(event->get_event_id()))
    {
      return true;
    }
  }

  return false;
}

bool Intention::is_finished()
{
  if (_suspended_by != nullptr)
  {
    return false;
  }
  else
  {
    return (_plans.size() == 0);
  }
}

bool Intention::is_suspended()
{
  return (_suspended_by != nullptr);
}

bool Intention::is_suspended_by_belief_event()
{
  return suspended_by_belief_event;
}

void Intention::terminate(BeliefBase * beliefs,
                          EventBase * events,
                          PlanBase * plans)
{
  if (events->is_full())
  {
    return;
    while (_plans.size() > 0)
    {
      _plans.pop_back();
    }
  }

  if ((beliefs == nullptr) || (events == nullptr) || (plans == nullptr))
  {
    return;
  }

  while (_plans.size() > 0)
  {
    Proposition prop(_plans.back()->get_plan()->get_proposition()->get_name());

    Event event(EventOperator::GOAL_DELETION, prop);
    Plan * plan = plans->revise(&event, beliefs);

    if (plan)
    {
      Event event(EventOperator::GOAL_DELETION, prop);
      events->add_event(event);
      while (_plans.size() > 0)
      {
        _plans.pop_back();
      }
      break;
    }
    else
    {
      _plans.pop_back();
    }
  }

  return;
}
