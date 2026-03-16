#ifndef CONFIGURATION_H_
#define CONFIGURATION_H_

#include "belief_base.h"
#include "event_base.h"
#include "plan_base.h"
#include "intention_base.h"
#include "functions.h"

class AgentSettings
{
private:
  Body body_0;
  Context context_0;
  Body body_1;
  Context context_1;
  Body body_2;
  Context context_2;
  BeliefBase belief_base;
  EventBase event_base;
  PlanBase plan_base;
  IntentionBase intention_base;

public:
  AgentSettings()
  {
    // Ajuste dos tamanhos conforme a necessidade do novo agente
    belief_base = BeliefBase(4);
    event_base = EventBase(5);
    plan_base = PlanBase(3);
    intention_base = IntentionBase(10, 4);

    // --- Proposições (Crenças) ---
    // 1: neighbor(MAC) - A existência de um vizinho (gerenciado externamente)
    // 2: has_capability(self, ULTRASONIC) - A própria capacidade
    // 3: obstacle_detected - Se um obstáculo foi detectado
    // 4: start - Meta para iniciar o comportamento do agente
    belief_base.add_belief(Belief(1, nullptr, false)); // neighbor
    belief_base.add_belief(Belief(2, nullptr, true));  // has_capability(self, ULTRASONIC)
    belief_base.add_belief(Belief(3, nullptr, false)); // obstacle_detected
    belief_base.add_belief(Belief(4, nullptr, false)); // start (meta)

    // --- Evento Inicial ---
    event_base.add_event(Event(EventOperator::GOAL_ADDITION, 4));

    // --- Planos ---

    // Plan 0: +!start <- show_ready_message.
    // Um plano simples para indicar que o agente iniciou corretamente.
    Proposition prop_0(4);
    context_0 = Context(0);
    body_0 = Body(1);
    body_0.add_instruction(BodyInstruction(BodyType::ACTION, Proposition(5), action_show_ready_message));
    Plan plan_0(EventOperator::GOAL_ADDITION, prop_0, &context_0, &body_0);
    plan_base.add_plan(plan_0);

    // Plan 1: +obstacle_detected(..) : true <- request_cooperation_alarm.
    // Quando a crença 'obstacle_detected' se torna verdadeira, este plano é acionado.
    // O corpo do plano executa a ação para solicitar cooperação (ex: soar um alarme).
    Proposition prop_1(3);
    context_1 = Context(0); // Sem contexto especial, sempre aplicável
    body_1 = Body(1);
    body_1.add_instruction(BodyInstruction(BodyType::ACTION, Proposition(6), action_request_cooperation_alarm));
    Plan plan_1(EventOperator::BELIEF_ADDITION, prop_1, &context_1, &body_1);
    plan_base.add_plan(plan_1);

    // Plan 2: -obstacle_detected(..) : true <- report_area_clear.
    // Quando a crença 'obstacle_detected' se torna falsa (obstáculo removido).
    // O corpo do plano executa a ação para relatar que a área está livre.
    Proposition prop_2(3);
    context_2 = Context(0); // Sem contexto especial
    body_2 = Body(1);
    body_2.add_instruction(BodyInstruction(BodyType::ACTION, Proposition(7), action_report_area_clear));
    Plan plan_2(EventOperator::BELIEF_DELETION, prop_2, &context_2, &body_2);
    plan_base.add_plan(plan_2);
  }

  BeliefBase * get_belief_base() { return &belief_base; }
  EventBase * get_event_base() { return &event_base; }
  PlanBase * get_plan_base() { return &plan_base; }
  IntentionBase * get_intention_base() { return &intention_base; }
};

#endif