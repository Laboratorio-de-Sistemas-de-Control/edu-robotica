/*
 * Vel_PI_Controller_private.h
 *
 * Academic Teaching License -- for classroom instructional use only.  Not
 * for academic research, government, commercial, or other organizational
 * use.
 *
 * Code generation for model "Vel_PI_Controller".
 *
 * Model version              : 20.2
 * Simulink Coder version : 25.2 (R2025b) 28-Jul-2025
 * C source code generated on : Fri May 15 17:46:11 2026
 *
 * Target selection: quarc_win64.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#ifndef Vel_PI_Controller_private_h_
#define Vel_PI_Controller_private_h_
#include "rtwtypes.h"
#include "multiword_types.h"
#include "zero_crossing_types.h"
#include "Vel_PI_Controller_types.h"

/* Used by FromWorkspace Block: '<Root>/From Workspace' */
#ifndef rtInterpolate
# define rtInterpolate(v1,v2,f1,f2)    (((v1)==(v2))?((double)(v1)): (((f1)*((double)(v1)))+((f2)*((double)(v2)))))
#endif

#ifndef rtRound
# define rtRound(v)                    ( ((v) >= 0) ? floor((v) + 0.5) : ceil((v) - 0.5) )
#endif

/* A global buffer for storing error messages (defined in quanser_common library) */
EXTERN char _rt_error_message[512];

/* private model entry point functions */
extern void Vel_PI_Controller_derivatives(void);

#endif                                 /* Vel_PI_Controller_private_h_ */
