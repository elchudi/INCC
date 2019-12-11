rm(list=ls()) #borro las cosas cargadas del Enviroment

#seteo el directorio de trabajo
# getwd() #me fijo en cual estoy
# setwd("/Lucca/Facu/INCC/Experimento/estadistica") # lo cambio


datoss = read.csv(file="data_digested.csv", header=TRUE, sep=",")
# datoss = datoss[datoss$self_assestment_expertise_score!= 4, ] # Borro a todos los que tienen 3 respuestas correctas
# datoss = datoss[datoss$self_assestment_expertise_score!= 5, ] # Borro a todos los que tienen 3 respuestas correctas
# datoss = datoss[datoss$self_assestment_expertise_score!= 7, ] # Borro a todos los que tienen 3 respuestas correctas
# datoss = datoss[datoss$weighted_expertise_score!= 6, ] # Borro a todos los que tienen 3 respuestas correctas
# datoss = datoss[datoss$q_correct_inmediato != 4, ]

# copio a un nuevo dataframe y transformo en factor
new_data <- data.frame(datoss$treatment, datoss$expert_inmediato, datoss$user, datoss$order, datoss$correct_binary, datoss$expert_self_assestment, datoss$expert_weighted)
names(new_data) <- c("treatment", "expert_inmediato", "user" , "order", "correct_binary", "expert_self_assestment", "expert_weighted")
library(lme4)
new_data$user <- factor(new_data$user)
new_data$treatment <- factor(new_data$treatment)
new_data$expert_inmediato <- factor(new_data$expert_inmediato)
new_data$expert_weighted <- factor(new_data$expert_weighted)
new_data$expert_self_assestment <- factor(new_data$expert_self_assestment)
new_data$correct_binary <- factor(new_data$correct_binary)


#### modelamo' ####

# m2 <-glmer(correct_binary ~ treatment * expertise  + order + (1|user), data=new_data, family=binomial) # medidas repetidas con modelo completo
#este modelo dice que no converge. Puede ser porque haya que centrar la variable cuanti o porque se esten estimando muchos parametros
# drop1(m2) # como baja el AIC cuando sacamos el factor 'orden', entonces conviene no ponerlo



# Quitando solo un pedazo

datoss = read.csv(file="data_digested.csv", header=TRUE, sep=",")
datoss = datoss[datoss$percentaje_difference > 17, ]
datoss = datoss[datoss$q_correct_inmediato != 3, ]
# datoss = datoss[datoss$q_correct_inmediato != 4, ]
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
m_percentage <- glmer(correct_binary ~ percentaje_difference + (1|user), data=new_data, family=binomial) # sin factor 'orden'
m_prereg <- glmer(correct_binary ~ treatment * expert_inmediato + order +  (1|user), data=new_data, family=binomial) # sin factor 'orden'
m_prereg_sin_order <- glmer(correct_binary ~ treatment * expert_inmediato +  (1|user), data=new_data, family=binomial) # sin factor 'orden'
m_prereg_sin_expert <- glmer(correct_binary ~ treatment +  (1|user), data=new_data, family=binomial) # sin factor 'orden'
summary(m_prereg)
summary(m_prereg_sin_order)
summary(m_prereg_sin_expert)




# Usando self assestment

datoss = read.csv(file="data_digested.csv", header=TRUE, sep=",")
# datoss = datoss[datoss$self_assestment_expertise_score != 4, ]
# datoss = datoss[datoss$self_assestment_expertise_score != 5, ]
datoss = datoss[datoss$percentaje_difference > 18, ]
new_data <- data.frame(datoss$treatment, datoss$expert_inmediato, datoss$user, datoss$order, datoss$correct_binary, datoss$expert_self_assestment, datoss$expert_weighted, datoss$percentaje_difference)
names(new_data) <- c("treatment", "expert_inmediato", "user" , "order", "correct_binary", "expert_self_assestment", "expert_weighted", "percentaje_difference")
library(lme4)
new_data$user <- factor(new_data$user)
new_data$treatment <- factor(new_data$treatment)
new_data$expert_inmediato <- factor(new_data$expert_inmediato)
new_data$expert_weighted <- factor(new_data$expert_weighted)
new_data$expert_self_assestment <- factor(new_data$expert_self_assestment)
new_data$correct_binary <- factor(new_data$correct_binary)
m <- glmer(correct_binary ~ treatment * expert_self_assestment +  (1|user), data=new_data, family=binomial) # sin factor 'orden'
summary(m)
e_weight_treatment <- glmer(correct_binary ~ expert_weighted * treatment + (1|user), data=new_data, family=binomial) # sin factor 'orden'
summary(e_weight_treatment )

for (i in :10){

}







m3 <- glmer(correct_binary ~ treatment * expert_self_assestment + (1|user), data=new_data, family=binomial) # sin factor 'orden'




e_self <- glmer(correct_binary ~ expert_self_assestment + (1|user), data=new_data, family=binomial) # sin factor 'orden'
e_weight <- glmer(correct_binary ~expert_weighted + (1|user), data=new_data, family=binomial) # sin factor 'orden'
e_inm <- glmer(correct_binary ~ expert_inmediato + (1|user), data=new_data, family=binomial) # sin factor 'orden'
#no da significativa nigun factor

summary(e_self)
summary(e_weight)
summary(e_inm)
# anova(m3)

e_self <- glmer(correct_binary ~ expert_self_assestment + (1|user), data=new_data, family=binomial) # sin factor 'orden'
e_self_glm <- glm(correct_binary ~ expert_self_assestment, data=new_data, family=binomial) # sin factor 'orden'
