#ifndef FUNCTIONS_H_
#define FUNCTIONS_H_

// Declaração da função de setup para os sensores/atuadores
void setup_hardware();

// Declarações das funções de percepção (sensores)
void check_sonic_sensor();

// Declarações das funções de ação do agente
bool action_show_ready_message();
bool action_request_cooperation_alarm();
bool action_report_area_clear();


#endif /* FUNCTIONS_H_ */