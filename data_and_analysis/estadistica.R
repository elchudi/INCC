rm(list=ls()) #borro las cosas cargadas del Enviroment

datoss = read.csv(file="data_digested.csv", header=TRUE, sep=",")
datoss = datoss[datoss$q_correct_inmediato != 4, ]
new_data <- data.frame(datoss$treatment, datoss$expert_inmediato, datoss$user, datoss$order, datoss$correct_binary, datoss$expert_self_assestment, datoss$expert_weighted, datoss$percentaje_difference)
names(new_data) <- c("treatment", "expert_inmediato", "user" , "order", "correct_binary", "expert_self_assestment", "expert_weighted", "percentaje_difference")
library(lme4)
new_data$user <- factor(new_data$user)
new_data$treatment <- factor(new_data$treatment)
new_data$expert_inmediato <- factor(new_data$expert_inmediato)
new_data$expert_weighted <- factor(new_data$expert_weighted)
new_data$expert_self_assestment <- factor(new_data$expert_self_assestment)
new_data$correct_binary <- factor(new_data$correct_binary)
new_data$correct_binary <- factor(new_data$correct_binary)
m_prereg <- glmer(correct_binary ~ treatment * expert_inmediato + order +  (1|user), data=new_data, family=binomial) # sin factor 'orden'
m_prereg_sin_order <- glmer(correct_binary ~ treatment * expert_inmediato +  (1|user), data=new_data, family=binomial) # sin factor 'orden'
summary(m_prereg)
summary(m_prereg_sin_order)
