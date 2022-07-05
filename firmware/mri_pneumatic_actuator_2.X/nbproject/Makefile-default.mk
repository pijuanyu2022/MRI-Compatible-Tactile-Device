#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Include project Makefile
ifeq "${IGNORE_LOCAL}" "TRUE"
# do not include local makefile. User is passing all local related variables already
else
include Makefile
# Include makefile containing local settings
ifeq "$(wildcard nbproject/Makefile-local-default.mk)" "nbproject/Makefile-local-default.mk"
include nbproject/Makefile-local-default.mk
endif
endif

# Environment
MKDIR=gnumkdir -p
RM=rm -f 
MV=mv 
CP=cp 

# Macros
CND_CONF=default
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
IMAGE_TYPE=debug
OUTPUT_SUFFIX=elf
DEBUGGABLE_SUFFIX=elf
FINAL_IMAGE=${DISTDIR}/mri_pneumatic_actuator_2.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
else
IMAGE_TYPE=production
OUTPUT_SUFFIX=hex
DEBUGGABLE_SUFFIX=elf
FINAL_IMAGE=${DISTDIR}/mri_pneumatic_actuator_2.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
endif

ifeq ($(COMPARE_BUILD), true)
COMPARISON_BUILD=-mafrlcsj
else
COMPARISON_BUILD=
endif

ifdef SUB_IMAGE_ADDRESS

else
SUB_IMAGE_ADDRESS_COMMAND=
endif

# Object Directory
OBJECTDIR=build/${CND_CONF}/${IMAGE_TYPE}

# Distribution Directory
DISTDIR=dist/${CND_CONF}/${IMAGE_TYPE}

# Source Files Quoted if spaced
SOURCEFILES_QUOTED_IF_SPACED=../src/main.c ../src/ili9341.c ../src/init.c ../src/adc.c ../src/uart.c

# Object Files Quoted if spaced
OBJECTFILES_QUOTED_IF_SPACED=${OBJECTDIR}/_ext/1360937237/main.o ${OBJECTDIR}/_ext/1360937237/ili9341.o ${OBJECTDIR}/_ext/1360937237/init.o ${OBJECTDIR}/_ext/1360937237/adc.o ${OBJECTDIR}/_ext/1360937237/uart.o
POSSIBLE_DEPFILES=${OBJECTDIR}/_ext/1360937237/main.o.d ${OBJECTDIR}/_ext/1360937237/ili9341.o.d ${OBJECTDIR}/_ext/1360937237/init.o.d ${OBJECTDIR}/_ext/1360937237/adc.o.d ${OBJECTDIR}/_ext/1360937237/uart.o.d

# Object Files
OBJECTFILES=${OBJECTDIR}/_ext/1360937237/main.o ${OBJECTDIR}/_ext/1360937237/ili9341.o ${OBJECTDIR}/_ext/1360937237/init.o ${OBJECTDIR}/_ext/1360937237/adc.o ${OBJECTDIR}/_ext/1360937237/uart.o

# Source Files
SOURCEFILES=../src/main.c ../src/ili9341.c ../src/init.c ../src/adc.c ../src/uart.c



CFLAGS=
ASFLAGS=
LDLIBSOPTIONS=

############# Tool locations ##########################################
# If you copy a project from one host to another, the path where the  #
# compiler is installed may be different.                             #
# If you open this project with MPLAB X in the new host, this         #
# makefile will be regenerated and the paths will be corrected.       #
#######################################################################
# fixDeps replaces a bunch of sed/cat/printf statements that slow down the build
FIXDEPS=fixDeps

.build-conf:  ${BUILD_SUBPROJECTS}
ifneq ($(INFORMATION_MESSAGE), )
	@echo $(INFORMATION_MESSAGE)
endif
	${MAKE}  -f nbproject/Makefile-default.mk ${DISTDIR}/mri_pneumatic_actuator_2.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}

MP_PROCESSOR_OPTION=32MX170F256B
MP_LINKER_FILE_OPTION=
# ------------------------------------------------------------------------------------
# Rules for buildStep: assemble
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: assembleWithPreprocess
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: compile
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${OBJECTDIR}/_ext/1360937237/main.o: ../src/main.c  .generated_files/flags/default/74dfaad34d577ac1fd0cd450af66167cad7d4910 .generated_files/flags/default/9ed7675dc3730fa0d7f1e23651b69559e876b3db
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/main.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/main.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG   -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -O1 -Werror -Wall -MP -MMD -MF "${OBJECTDIR}/_ext/1360937237/main.o.d" -o ${OBJECTDIR}/_ext/1360937237/main.o ../src/main.c    -DXPRJ_default=$(CND_CONF)  -no-legacy-libc  $(COMPARISON_BUILD)    
	
${OBJECTDIR}/_ext/1360937237/ili9341.o: ../src/ili9341.c  .generated_files/flags/default/76f1c81ec837247ad38d326e80b5ba60b3f64988 .generated_files/flags/default/9ed7675dc3730fa0d7f1e23651b69559e876b3db
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/ili9341.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/ili9341.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG   -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -O1 -Werror -Wall -MP -MMD -MF "${OBJECTDIR}/_ext/1360937237/ili9341.o.d" -o ${OBJECTDIR}/_ext/1360937237/ili9341.o ../src/ili9341.c    -DXPRJ_default=$(CND_CONF)  -no-legacy-libc  $(COMPARISON_BUILD)    
	
${OBJECTDIR}/_ext/1360937237/init.o: ../src/init.c  .generated_files/flags/default/f9ae8d8f613a75aca498ba69ec35a5668c80a719 .generated_files/flags/default/9ed7675dc3730fa0d7f1e23651b69559e876b3db
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/init.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/init.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG   -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -O1 -Werror -Wall -MP -MMD -MF "${OBJECTDIR}/_ext/1360937237/init.o.d" -o ${OBJECTDIR}/_ext/1360937237/init.o ../src/init.c    -DXPRJ_default=$(CND_CONF)  -no-legacy-libc  $(COMPARISON_BUILD)    
	
${OBJECTDIR}/_ext/1360937237/adc.o: ../src/adc.c  .generated_files/flags/default/666a13c43970ea8ca19ff9ac582b9752efa2f8e5 .generated_files/flags/default/9ed7675dc3730fa0d7f1e23651b69559e876b3db
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/adc.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/adc.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG   -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -O1 -Werror -Wall -MP -MMD -MF "${OBJECTDIR}/_ext/1360937237/adc.o.d" -o ${OBJECTDIR}/_ext/1360937237/adc.o ../src/adc.c    -DXPRJ_default=$(CND_CONF)  -no-legacy-libc  $(COMPARISON_BUILD)    
	
${OBJECTDIR}/_ext/1360937237/uart.o: ../src/uart.c  .generated_files/flags/default/9c49e2ddb1dbfdeeb770121381880c9ac56fb7f1 .generated_files/flags/default/9ed7675dc3730fa0d7f1e23651b69559e876b3db
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/uart.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/uart.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG   -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -O1 -Werror -Wall -MP -MMD -MF "${OBJECTDIR}/_ext/1360937237/uart.o.d" -o ${OBJECTDIR}/_ext/1360937237/uart.o ../src/uart.c    -DXPRJ_default=$(CND_CONF)  -no-legacy-libc  $(COMPARISON_BUILD)    
	
else
${OBJECTDIR}/_ext/1360937237/main.o: ../src/main.c  .generated_files/flags/default/b69ccd59c57b35897d877da1243af20f7973a83d .generated_files/flags/default/9ed7675dc3730fa0d7f1e23651b69559e876b3db
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/main.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/main.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -O1 -Werror -Wall -MP -MMD -MF "${OBJECTDIR}/_ext/1360937237/main.o.d" -o ${OBJECTDIR}/_ext/1360937237/main.o ../src/main.c    -DXPRJ_default=$(CND_CONF)  -no-legacy-libc  $(COMPARISON_BUILD)    
	
${OBJECTDIR}/_ext/1360937237/ili9341.o: ../src/ili9341.c  .generated_files/flags/default/ec86a69b5bf5030966b61971b8b267728d46717f .generated_files/flags/default/9ed7675dc3730fa0d7f1e23651b69559e876b3db
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/ili9341.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/ili9341.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -O1 -Werror -Wall -MP -MMD -MF "${OBJECTDIR}/_ext/1360937237/ili9341.o.d" -o ${OBJECTDIR}/_ext/1360937237/ili9341.o ../src/ili9341.c    -DXPRJ_default=$(CND_CONF)  -no-legacy-libc  $(COMPARISON_BUILD)    
	
${OBJECTDIR}/_ext/1360937237/init.o: ../src/init.c  .generated_files/flags/default/163a6908d1b0bb9a619104fe6d5167ef7d99b1d .generated_files/flags/default/9ed7675dc3730fa0d7f1e23651b69559e876b3db
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/init.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/init.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -O1 -Werror -Wall -MP -MMD -MF "${OBJECTDIR}/_ext/1360937237/init.o.d" -o ${OBJECTDIR}/_ext/1360937237/init.o ../src/init.c    -DXPRJ_default=$(CND_CONF)  -no-legacy-libc  $(COMPARISON_BUILD)    
	
${OBJECTDIR}/_ext/1360937237/adc.o: ../src/adc.c  .generated_files/flags/default/54adbbaf04bb585455c5fa01628a9928317f1152 .generated_files/flags/default/9ed7675dc3730fa0d7f1e23651b69559e876b3db
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/adc.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/adc.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -O1 -Werror -Wall -MP -MMD -MF "${OBJECTDIR}/_ext/1360937237/adc.o.d" -o ${OBJECTDIR}/_ext/1360937237/adc.o ../src/adc.c    -DXPRJ_default=$(CND_CONF)  -no-legacy-libc  $(COMPARISON_BUILD)    
	
${OBJECTDIR}/_ext/1360937237/uart.o: ../src/uart.c  .generated_files/flags/default/fc842b9f4cdabe7fc0746faf626c355ca3e9c0ba .generated_files/flags/default/9ed7675dc3730fa0d7f1e23651b69559e876b3db
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/uart.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/uart.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -O1 -Werror -Wall -MP -MMD -MF "${OBJECTDIR}/_ext/1360937237/uart.o.d" -o ${OBJECTDIR}/_ext/1360937237/uart.o ../src/uart.c    -DXPRJ_default=$(CND_CONF)  -no-legacy-libc  $(COMPARISON_BUILD)    
	
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: compileCPP
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: link
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${DISTDIR}/mri_pneumatic_actuator_2.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk    
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE) -g   -mprocessor=$(MP_PROCESSOR_OPTION)  -o ${DISTDIR}/mri_pneumatic_actuator_2.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX} ${OBJECTFILES_QUOTED_IF_SPACED}          -DXPRJ_default=$(CND_CONF)  -no-legacy-libc  $(COMPARISON_BUILD)   -mreserve=data@0x0:0x1FC -mreserve=boot@0x1FC00490:0x1FC00BEF  -Wl,--defsym=__MPLAB_BUILD=1$(MP_EXTRA_LD_POST)$(MP_LINKER_FILE_OPTION),--defsym=__MPLAB_DEBUG=1,--defsym=__DEBUG=1,-D=__DEBUG_D,--gc-sections,--no-code-in-dinit,--no-dinit-in-serial-mem,-Map="${DISTDIR}/${PROJECTNAME}.${IMAGE_TYPE}.map",--memorysummary,${DISTDIR}/memoryfile.xml 
	
else
${DISTDIR}/mri_pneumatic_actuator_2.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk   
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE)  -mprocessor=$(MP_PROCESSOR_OPTION)  -o ${DISTDIR}/mri_pneumatic_actuator_2.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX} ${OBJECTFILES_QUOTED_IF_SPACED}          -DXPRJ_default=$(CND_CONF)  -no-legacy-libc  $(COMPARISON_BUILD)  -Wl,--defsym=__MPLAB_BUILD=1$(MP_EXTRA_LD_POST)$(MP_LINKER_FILE_OPTION),--gc-sections,--no-code-in-dinit,--no-dinit-in-serial-mem,-Map="${DISTDIR}/${PROJECTNAME}.${IMAGE_TYPE}.map",--memorysummary,${DISTDIR}/memoryfile.xml 
	${MP_CC_DIR}\\xc32-bin2hex ${DISTDIR}/mri_pneumatic_actuator_2.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX} 
endif


# Subprojects
.build-subprojects:


# Subprojects
.clean-subprojects:

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r ${OBJECTDIR}
	${RM} -r ${DISTDIR}

# Enable dependency checking
.dep.inc: .depcheck-impl

DEPFILES=$(shell mplabwildcard ${POSSIBLE_DEPFILES})
ifneq (${DEPFILES},)
include ${DEPFILES}
endif
