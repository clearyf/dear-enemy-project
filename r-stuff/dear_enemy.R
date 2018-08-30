# packages require to do GLMER
installed.packages("lme4")
installed.packages("nlme")
installed.packages("blmeco")
installed.packages("multcomp")
library("lme4")
library("nlme")
library("blmeco")
library("multcomp")

# Import csv file to R
data<-read.csv("complete_output_data-dear_enemy-1.csv")

# Data organization
data$phase<-factor(data$phase,levels = c("habituation","experiment"))
data$cond<-factor(data$phase,levels = c("control","treatment"))
data$subject<-factor(data$subject,levels = c("m","f","nm","nf"))
data$pairid<-as.factor(data$pairid)

str(data) # check data structure

# Generalized linear mixed models
# app_int<-glmer(app_int~phase+cond+(1|pairid), data=data, family=poisson)
app_int<-glmer(app_int ~ (1|pairid), data=data, family=poisson)

hist(data$app_int)
summary(app_int)
dispersion_glmer(app_int)

# Boxplot - graphs - code
# boxplot(totalagg~exphase,data=data,outline=FALSE)
# boxplot(cavity~exphase,data=data,outline=FALSE)
# boxplot(nestmaint~exphase,data=data,outline=FALSE)
# boxplot(nestdef~exphase,data=data,outline=FALSE)

