import csv
import os

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('./') if isfile(join('./', f))]
onlycsv = [x for x in onlyfiles if x[-4:] == ".csv" and "data_digested" not in x and 'row_per_user' not in x]
print(len(onlycsv))

INM = "inmediato"
CON = "consciente"
INCONS = "inconsciente"
subject_count = 1
all_data = []
for filename in onlycsv:
    
    with open(filename, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',')
        rows = [row for row in spamreader]
    for x in rows:
        for k,v in x.items():
            if v == "None":
                x[k] = None
    # print(rows[0])
    n_back_training = rows[:10]
    # print(n_back_training)
    to_ret = {}
    to_ret['subject'] = subject_count
    to_ret['filename'] = filename
    subject_count += 1
    q_nback_training = 0
    for x in n_back_training:
        if x['corresp']  and x['nback_train_resp.keys']:
            q_nback_training += 1
    # print(f'q_nback_training:{q_nback_training}')
    to_ret['q_correct_nback_training'] = q_nback_training
    to_ret['group'] = rows[0]['group']
    to_ret['self_assestment_expertise_score'] = int(rows[-1]['key_resp_2.keys'])
    to_ret['bimbo_question_correct'] = rows[-1]['respuesta3bis_3.keys'] == 'c' # TODO is this the correct option?
    to_ret['q_supermercador_trip'] = int(rows[-1]['respuesta1.keys'])
    # print(to_ret)
    treatment_order_indexes = sorted(set([int(x['treatment_order.thisIndex']) for x in rows if x['treatment_order.thisIndex']]))
    # print(treatment_order_indexes)
    per_treatment = []
    order = 1
    for treatment_order_index in treatment_order_indexes:
        data = {'user': filename, 'order': order}
        order +=1
        responses = [x for x in rows if x['treatment_order.thisIndex'] == str(treatment_order_index)]
        # data[treatment_order_index] = responses
        # print(treatment_order_index, len(responses))
        correcta = responses[0]['correcta']
        data['correct_answer'] = correcta
        if len(responses) > 2:
            assert all([x['inconsciente'] == '1' for x in responses])
            assert responses[-2]['key_resp.keys'] in ['left', 'right']
            data['user_response'] = responses[-2]['key_resp.keys']
            data['treatment'] = INCONS
        elif len(responses) == 2:
            if treatment_order_index <= 11:
                assert all([x['consciente'] == '1' for x in responses])
                assert responses[0]['respuesta_consciente.keys'] in ['left', 'right']
                data['user_response'] = responses[0]['respuesta_consciente.keys']
                data['treatment'] = CON
            else:
                assert all([x['inmediato'] == '1' for x in responses])
                assert responses[0]['respuesta_inmediato.keys'] in ['left', 'right']
                data['user_response'] = responses[0]['respuesta_inmediato.keys']
                data['treatment'] = INM
        data['user_responded_correctly'] = data['user_response'] == data['correct_answer']
        data['user_info'] = to_ret
        print(data)
        per_treatment.append(data)
        if data['treatment'] != 'inmediato':
            all_data.append(data)
    """
    inmediato = [x for x in per_treatment if x['treatment'] == "inmediato"]
    consciente = [x for x in per_treatment if x['treatment'] == "consciente"]
    inconsciente = [x for x in per_treatment if x['treatment'] == "insconciente"]
    """
    for t in [INM, CON, INCONS]:
        q_correct_answers = sum([1 for x in [x for x in per_treatment if x['treatment'] == t] if x['user_responded_correctly']])
        to_ret['q_correct_' + t] = q_correct_answers
    # print(filename, ',', to_ret['q_correct_inconsciente'])
    print(to_ret)

    """
    for x in per_treatment:
        print(x)
    """


with open('two_row_per_user.csv', 'w', newline='') as two_row_per_user:
    
    fieldnames_two_per_user = ['user', 'q_correct_inmediato', 'treatment_group', 'self_assestment_expertise_score', 'bimbo_question_correct', 'q_supermercador_trip', 'weighted_expertise_score', 'all_treatments_q_correct', 'con_incons_q_correct', 'expert_weighted', 'expert_inmediato', 'expert_self_assestment']
    for t in [INM, CON, INCONS]:
        fieldnames_two_per_user = fieldnames_two_per_user + ['q_correct_' + t]
    writer_two_user_per_row = csv.DictWriter(two_row_per_user, fieldnames=fieldnames_two_per_user, extrasaction='ignore')
    writer_two_user_per_row.writeheader()

    with open('one_row_per_user.csv', 'w', newline='') as one_row_per_user:
        
        fieldnames_one_per_user = ['user', 'q_correct_inmediato', 'treatment_group', 'self_assestment_expertise_score', 'bimbo_question_correct', 'q_supermercador_trip', 'weighted_expertise_score', 'all_treatments_q_correct', 'con_incons_q_correct', 'expert_weighted', 'expert_inmediato', 'expert_self_assestment']
        for t in [INM, CON, INCONS]:
            fieldnames_one_per_user = fieldnames_one_per_user + ['q_correct_' + t]
        writer_one_user_per_row = csv.DictWriter(one_row_per_user, fieldnames=fieldnames_one_per_user, extrasaction='ignore')
        writer_one_user_per_row.writeheader()
        with open('data_digested.csv', 'w', newline='') as csvfile:
            fieldnames = ['correct_binary', 'user', 'order', 'treatment', 'q_correct_inmediato', 'user_responded_correctly', 'treatment_group', 'previous_treatment', 'self_assestment_expertise_score', 'bimbo_question_correct', 'q_supermercador_trip', 'weighted_expertise_score', 'all_treatments_q_correct', 'con_incons_q_correct', 'expert_weighted', 'expert_inmediato', 'expert_self_assestment']
            for t in [INM, CON, INCONS]:
                fieldnames = fieldnames + ['q_correct_' + t]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            user = None
            for x in all_data:
                if user != x['user']:
                    user = x['user']
                    previous_treatment = None
                    write_to_one_per_row = True
                    
                x['correct_binary'] = 1 if x['user_responded_correctly'] else 0
                x['q_correct_inmediato'] = x['user_info']['q_correct_inmediato']
                x['treatment_group'] = x['user_info']['group']
                x['previous_treatment'] = previous_treatment
                x['self_assestment_expertise_score'] = x['user_info']['self_assestment_expertise_score']
                x['bimbo_question_correct'] = x['user_info']['bimbo_question_correct']
                x['q_supermercador_trip'] = x['user_info']['q_supermercador_trip']
                total_correct = 0
                for t in [INM, CON, INCONS]:
                    x['q_correct_' + t] = int(x['user_info']['q_correct_' + t])
                    total_correct += x['q_correct_' + t]
                    x['all_treatments_q_correct'] = total_correct
                x['con_incons_q_correct'] = x['q_correct_' + CON] + x['q_correct_' + INCONS]


                weighted_expertise = float(x['q_correct_inmediato'])
                if x['self_assestment_expertise_score'] <= 2:
                    pass
                elif x['self_assestment_expertise_score'] <= 5:
                    weighted_expertise += 1
                else:
                    weighted_expertise += 2

                if x['q_supermercador_trip'] <= 1:
                    pass
                elif x['q_supermercador_trip'] <= 4:
                    weighted_expertise += 1
                else:
                    weighted_expertise += 2

                if x['bimbo_question_correct']:
                    weighted_expertise += 1

                x['weighted_expertise_score'] = weighted_expertise
                x['expert_weighted'] = 1 if int(weighted_expertise) >= 6 else 0
                x['expert_inmediato'] = 1 if int(x['q_correct_inmediato']) >= 4 else 0
                x['expert_self_assestment'] = 1 if int(x['self_assestment_expertise_score']) >= 5 else 0
                
                previous_treatment = x['treatment']
                writer.writerow(x)
                if write_to_one_per_row:
                    writer_one_user_per_row.writerow(x)
                    to_print = {}
                    to_print['user'] = x['user']
                    to_print['value'] = x['user']
                    x['q_correct_' + t] = int(x['user_info']['q_correct_' + t])
                    to_print['user'] = x['user']
                    writer_two_user_per_row.writerow(x)
                    writer_two_user_per_row.writerow(x)
                    write_to_one_per_row = False
