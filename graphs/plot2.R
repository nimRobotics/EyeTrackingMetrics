library("ggplot2")
library("reshape2")
library(dplyr)

gaze <- read.csv("gazedata.csv", header=TRUE)

summary(gaze)

gaze<-reshape(gaze, 
        direction = "long",
        varying = list(names(gaze)[3:ncol(gaze)]),
        v.names = "Value",
        idvar = c("ID", "Gender"))

gaze<-gaze %>% mutate(entropytype =
                     case_when(time <= 20 ~ "SGE", 
                               time >= 21 ~ "GTE"),
                trialtype =
                     case_when(time <= 10 ~ "normal", 
                               time <= 20 ~ "attack",
                               time <= 30 ~ "normal",
                               time <= 40 ~ "attack"))

summary(gaze)

SGE<-gaze[gaze$entropytype=="SGE",]
GTE<-gaze[gaze$entropytype=="GTE",]

require(ggplot2)
jpeg("sge.jpg", width = 1920, height = 1080)
box<- ggplot(data=SGE, aes(x=ID, y=Value))+
	geom_boxplot(notch = FALSE, width=.4, aes(fill=trialtype))+
	labs(title="Gaze entropy",x = "Participants", y = "SGE")+
	geom_jitter(size = 1, alpha = 0.1, width = 0.2)+
	theme(axis.title = element_text(size = 32), 
        axis.text = element_text(size = 26),
        plot.title = element_text(size=32),
        legend.key.size = unit(3, 'cm'), #change legend key size
        legend.title = element_text(size=26), #change legend title font size
        legend.text = element_text(size=26)) #change legend text font size
box
dev.off() 

require(ggplot2)
jpeg("gte.jpg", width = 1920, height = 1080)
box<- ggplot(data=GTE, aes(x=ID, y=Value))+
	geom_boxplot(notch = FALSE, width=.4, aes(fill=trialtype))+
	labs(title="Gaze entropy",x = "Participants", y = "GTE")+
	geom_jitter(size = 1, alpha = 0.1, width = 0.2)+
	theme(axis.title = element_text(size = 32), 
        axis.text = element_text(size = 26),
        plot.title = element_text(size=32),
        legend.key.size = unit(3, 'cm'), #change legend key size
        legend.title = element_text(size=26), #change legend title font size
        legend.text = element_text(size=26)) #change legend text font size
box
dev.off() 

require(ggplot2)
jpeg("gte_avg.jpg", width = 1920, height = 1080)
box<- ggplot(data=SGE, aes(x=trialtype, y=Value))+
	geom_boxplot(notch = FALSE, width=.4)+
	labs(title="Gaze entropy",x = "Trials", y = "GTE")+
	geom_jitter(size = 1, alpha = 0.1, width = 0.2)+
	theme(axis.title = element_text(size = 32), 
        axis.text = element_text(size = 26),
        plot.title = element_text(size=32),
        legend.key.size = unit(3, 'cm'), #change legend key size
        legend.title = element_text(size=26), #change legend title font size
        legend.text = element_text(size=26)) #change legend text font size
box
dev.off() 

require(ggplot2)
jpeg("sge_avg.jpg", width = 1920, height = 1080)
box<- ggplot(data=GTE, aes(x=trialtype, y=Value))+
	geom_boxplot(notch = FALSE, width=.4)+
	labs(title="Gaze entropy",x = "Trials", y = "SGE")+
	geom_jitter(size = 1, alpha = 0.1, width = 0.2)+
	theme(axis.title = element_text(size = 32), 
        axis.text = element_text(size = 26),
        plot.title = element_text(size=32),
        legend.key.size = unit(3, 'cm'), #change legend key size
        legend.title = element_text(size=26), #change legend title font size
        legend.text = element_text(size=26)) #change legend text font size
box
dev.off() 




SGEnormal<-SGE[SGE$trialtype=="normal",]
SGEattack<-SGE[SGE$trialtype=="attack",]

res <- t.test(SGEnormal$Value, SGEattack$Value, paired = TRUE, alternative = "less")
res



GTEnormal<-GTE[GTE$trialtype=="normal",]
GTEattack<-GTE[GTE$trialtype=="attack",]

res <- t.test(GTEnormal$Value, GTEattack$Value, paired = TRUE, alternative = "greater")
res



jpeg("sge_trialwise.jpg", width = 1920, height = 1080)
# Visualization
linebox<-ggplot(SGE, aes(x = time, y = Value)) + 
  geom_line(aes(color = ID, linetype = ID)) +
  #  + scale_color_manual(values = c("darkred", "steelblue"))
  labs(title="Gaze entropy vs Trials",x = "Trials", y = "SGE") +
  theme(axis.title = element_text(size = 32), 
        axis.text = element_text(size = 26),
        plot.title = element_text(size=32),
        # legend.key.size = unit(3, 'cm'), #change legend key size
        legend.title = element_text(size=26), #change legend title font size
        legend.text = element_text(size=26)) #change legend text font size
linebox
dev.off()


jpeg("gte_trialwise.jpg", width = 1920, height = 1080)
# Visualization
ggplot(GTE, aes(x = time, y = Value)) + 
  geom_line(aes(color = ID, linetype = ID))+
  labs(title="Gaze entropy vs Trials",x = "Trials", y = "SGE") +
  theme(axis.title = element_text(size = 32), 
        axis.text = element_text(size = 26),
        plot.title = element_text(size=32),
        # legend.key.size = unit(3, 'cm'), #change legend key size
        legend.title = element_text(size=26), #change legend title font size
        legend.text = element_text(size=26)) #change legend text font size
dev.off()