#ifndef FUNCTIONS_H_
#define FUNCTIONS_H_

// Declaração da função de setup para os atuadores
void setup_actions();

// Declarações das funções de ação do agente
bool action_show_ready_message();
bool action_led_on();
bool action_led_off();

// Declarações das funções de ação de cooperação
bool action_send_cooperation_response();

#endif /* FUNCTIONS_H_ */