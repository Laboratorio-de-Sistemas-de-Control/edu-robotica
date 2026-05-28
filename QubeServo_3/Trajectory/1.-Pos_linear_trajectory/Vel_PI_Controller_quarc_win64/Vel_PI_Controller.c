/*
 * Vel_PI_Controller.c
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

#include "Vel_PI_Controller.h"
#include "rtwtypes.h"
#include "Vel_PI_Controller_private.h"
#include <string.h>
#include "Vel_PI_Controller_dt.h"

/* Block signals (default storage) */
B_Vel_PI_Controller_T Vel_PI_Controller_B;

/* Continuous states */
X_Vel_PI_Controller_T Vel_PI_Controller_X;

/* Disabled State Vector */
XDis_Vel_PI_Controller_T Vel_PI_Controller_XDis;

/* Block states (default storage) */
DW_Vel_PI_Controller_T Vel_PI_Controller_DW;

/* Real-time model */
static RT_MODEL_Vel_PI_Controller_T Vel_PI_Controller_M_;
RT_MODEL_Vel_PI_Controller_T *const Vel_PI_Controller_M = &Vel_PI_Controller_M_;

/*
 * This function updates continuous states using the ODE3 fixed-step
 * solver algorithm
 */
static void rt_ertODEUpdateContinuousStates(RTWSolverInfo *si )
{
  /* Solver Matrices */
  static const real_T rt_ODE3_A[3] = {
    1.0/2.0, 3.0/4.0, 1.0
  };

  static const real_T rt_ODE3_B[3][3] = {
    { 1.0/2.0, 0.0, 0.0 },

    { 0.0, 3.0/4.0, 0.0 },

    { 2.0/9.0, 1.0/3.0, 4.0/9.0 }
  };

  time_T t = rtsiGetT(si);
  time_T tnew = rtsiGetSolverStopTime(si);
  time_T h = rtsiGetStepSize(si);
  real_T *x = rtsiGetContStates(si);
  ODE3_IntgData *id = (ODE3_IntgData *)rtsiGetSolverData(si);
  real_T *y = id->y;
  real_T *f0 = id->f[0];
  real_T *f1 = id->f[1];
  real_T *f2 = id->f[2];
  real_T hB[3];
  int_T i;
  int_T nXc = 1;
  rtsiSetSimTimeStep(si,MINOR_TIME_STEP);

  /* Save the state values at time t in y, we'll use x as ynew. */
  (void) memcpy(y, x,
                (uint_T)nXc*sizeof(real_T));

  /* Assumes that rtsiSetT and ModelOutputs are up-to-date */
  /* f0 = f(t,y) */
  rtsiSetdX(si, f0);
  Vel_PI_Controller_derivatives();

  /* f(:,2) = feval(odefile, t + hA(1), y + f*hB(:,1), args(:)(*)); */
  hB[0] = h * rt_ODE3_B[0][0];
  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0]);
  }

  rtsiSetT(si, t + h*rt_ODE3_A[0]);
  rtsiSetdX(si, f1);
  Vel_PI_Controller_output();
  Vel_PI_Controller_derivatives();

  /* f(:,3) = feval(odefile, t + hA(2), y + f*hB(:,2), args(:)(*)); */
  for (i = 0; i <= 1; i++) {
    hB[i] = h * rt_ODE3_B[1][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1]);
  }

  rtsiSetT(si, t + h*rt_ODE3_A[1]);
  rtsiSetdX(si, f2);
  Vel_PI_Controller_output();
  Vel_PI_Controller_derivatives();

  /* tnew = t + hA(3);
     ynew = y + f*hB(:,3); */
  for (i = 0; i <= 2; i++) {
    hB[i] = h * rt_ODE3_B[2][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1] + f2[i]*hB[2]);
  }

  rtsiSetT(si, tnew);
  rtsiSetSimTimeStep(si,MAJOR_TIME_STEP);
}

/* Model output function */
void Vel_PI_Controller_output(void)
{
  real_T rtb_HILReadTimebase_o1;
  real_T rtb_HILReadTimebase_o2;
  boolean_T tmp;
  if (rtmIsMajorTimeStep(Vel_PI_Controller_M)) {
    /* set solver stop time */
    if (!(Vel_PI_Controller_M->Timing.clockTick0+1)) {
      rtsiSetSolverStopTime(&Vel_PI_Controller_M->solverInfo,
                            ((Vel_PI_Controller_M->Timing.clockTickH0 + 1) *
        Vel_PI_Controller_M->Timing.stepSize0 * 4294967296.0));
    } else {
      rtsiSetSolverStopTime(&Vel_PI_Controller_M->solverInfo,
                            ((Vel_PI_Controller_M->Timing.clockTick0 + 1) *
        Vel_PI_Controller_M->Timing.stepSize0 +
        Vel_PI_Controller_M->Timing.clockTickH0 *
        Vel_PI_Controller_M->Timing.stepSize0 * 4294967296.0));
    }
  }                                    /* end MajorTimeStep */

  /* Update absolute time of base rate at minor time step */
  if (rtmIsMinorTimeStep(Vel_PI_Controller_M)) {
    Vel_PI_Controller_M->Timing.t[0] = rtsiGetT(&Vel_PI_Controller_M->solverInfo);
  }

  tmp = rtmIsMajorTimeStep(Vel_PI_Controller_M);
  if (tmp) {
    /* S-Function (hil_read_timebase_block): '<Root>/HIL Read Timebase' */

    /* S-Function Block: Vel_PI_Controller/HIL Read Timebase (hil_read_timebase_block) */
    {
      t_error result;
      result = hil_task_read(Vel_PI_Controller_DW.HILReadTimebase_Task, 1,
        NULL,
        &Vel_PI_Controller_DW.HILReadTimebase_EncoderBuffer,
        NULL,
        &Vel_PI_Controller_DW.HILReadTimebase_OtherBuffer
        );
      if (result < 0) {
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
      } else {
        rtb_HILReadTimebase_o1 =
          Vel_PI_Controller_DW.HILReadTimebase_EncoderBuffer;
        rtb_HILReadTimebase_o2 =
          Vel_PI_Controller_DW.HILReadTimebase_OtherBuffer;
      }
    }
  }

  /* FromWorkspace: '<Root>/From Workspace' */
  {
    real_T *pDataValues = (real_T *)
      Vel_PI_Controller_DW.FromWorkspace_PWORK.DataPtr;
    real_T *pTimeValues = (real_T *)
      Vel_PI_Controller_DW.FromWorkspace_PWORK.TimePtr;
    int_T currTimeIndex = Vel_PI_Controller_DW.FromWorkspace_IWORK.PrevIndex;
    real_T t = Vel_PI_Controller_M->Timing.t[0];

    /* Get index */
    if (t <= pTimeValues[0]) {
      currTimeIndex = 0;
    } else if (t >= pTimeValues[50]) {
      currTimeIndex = 49;
    } else {
      if (t < pTimeValues[currTimeIndex]) {
        while (t < pTimeValues[currTimeIndex]) {
          currTimeIndex--;
        }
      } else {
        while (t >= pTimeValues[currTimeIndex + 1]) {
          currTimeIndex++;
        }
      }
    }

    Vel_PI_Controller_DW.FromWorkspace_IWORK.PrevIndex = currTimeIndex;

    /* Post output */
    {
      real_T t1 = pTimeValues[currTimeIndex];
      real_T t2 = pTimeValues[currTimeIndex + 1];
      if (t1 == t2) {
        if (t < t1) {
          Vel_PI_Controller_B.FromWorkspace = pDataValues[currTimeIndex];
        } else {
          Vel_PI_Controller_B.FromWorkspace = pDataValues[currTimeIndex + 1];
        }
      } else {
        real_T f1 = (t2 - t) / (t2 - t1);
        real_T f2 = 1.0 - f1;
        real_T d1;
        real_T d2;
        int_T TimeIndex = currTimeIndex;
        d1 = pDataValues[TimeIndex];
        d2 = pDataValues[TimeIndex + 1];
        Vel_PI_Controller_B.FromWorkspace = (real_T) rtInterpolate(d1, d2, f1,
          f2);
        pDataValues += 51;
      }
    }
  }

  if (tmp) {
    /* Gain: '<Root>/Gain1' */
    Vel_PI_Controller_B.Gain1 = Vel_PI_Controller_P.Gain1_Gain *
      rtb_HILReadTimebase_o2;

    /* Gain: '<Root>/Gain2' */
    Vel_PI_Controller_B.Gain2 = Vel_PI_Controller_P.Gain2_Gain *
      rtb_HILReadTimebase_o1;
  }

  /* Sum: '<Root>/Sum' */
  Vel_PI_Controller_B.Sum = Vel_PI_Controller_B.FromWorkspace -
    Vel_PI_Controller_B.Gain1;

  /* Sum: '<Root>/Sum of Elements' incorporates:
   *  Gain: '<Root>/Gain'
   *  TransferFcn: '<Root>/Transfer Fcn'
   */
  rtb_HILReadTimebase_o1 = Vel_PI_Controller_P.Gain_Gain *
    Vel_PI_Controller_B.Sum + Vel_PI_Controller_P.TransferFcn_C *
    Vel_PI_Controller_X.TransferFcn_CSTATE;

  /* Saturate: '<Root>/Saturation' */
  if (rtb_HILReadTimebase_o1 > Vel_PI_Controller_P.Saturation_UpperSat) {
    /* Saturate: '<Root>/Saturation' */
    Vel_PI_Controller_B.Saturation = Vel_PI_Controller_P.Saturation_UpperSat;
  } else if (rtb_HILReadTimebase_o1 < Vel_PI_Controller_P.Saturation_LowerSat) {
    /* Saturate: '<Root>/Saturation' */
    Vel_PI_Controller_B.Saturation = Vel_PI_Controller_P.Saturation_LowerSat;
  } else {
    /* Saturate: '<Root>/Saturation' */
    Vel_PI_Controller_B.Saturation = rtb_HILReadTimebase_o1;
  }

  /* End of Saturate: '<Root>/Saturation' */
  if (tmp) {
    /* S-Function (hil_write_analog_block): '<Root>/HIL Write Analog' */

    /* S-Function Block: Vel_PI_Controller/HIL Write Analog (hil_write_analog_block) */
    {
      t_error result;
      result = hil_write_analog(Vel_PI_Controller_DW.HILInitialize_Card,
        &Vel_PI_Controller_P.HILWriteAnalog_channels, 1,
        &Vel_PI_Controller_B.Saturation);
      if (result < 0) {
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
      }
    }
  }
}

/* Model update function */
void Vel_PI_Controller_update(void)
{
  if (rtmIsMajorTimeStep(Vel_PI_Controller_M)) {
    rt_ertODEUpdateContinuousStates(&Vel_PI_Controller_M->solverInfo);
  }

  /* Update absolute time for base rate */
  /* The "clockTick0" counts the number of times the code of this task has
   * been executed. The absolute time is the multiplication of "clockTick0"
   * and "Timing.stepSize0". Size of "clockTick0" ensures timer will not
   * overflow during the application lifespan selected.
   * Timer of this task consists of two 32 bit unsigned integers.
   * The two integers represent the low bits Timing.clockTick0 and the high bits
   * Timing.clockTickH0. When the low bit overflows to 0, the high bits increment.
   */
  if (!(++Vel_PI_Controller_M->Timing.clockTick0)) {
    ++Vel_PI_Controller_M->Timing.clockTickH0;
  }

  Vel_PI_Controller_M->Timing.t[0] = rtsiGetSolverStopTime
    (&Vel_PI_Controller_M->solverInfo);

  {
    /* Update absolute timer for sample time: [0.002s, 0.0s] */
    /* The "clockTick1" counts the number of times the code of this task has
     * been executed. The absolute time is the multiplication of "clockTick1"
     * and "Timing.stepSize1". Size of "clockTick1" ensures timer will not
     * overflow during the application lifespan selected.
     * Timer of this task consists of two 32 bit unsigned integers.
     * The two integers represent the low bits Timing.clockTick1 and the high bits
     * Timing.clockTickH1. When the low bit overflows to 0, the high bits increment.
     */
    if (!(++Vel_PI_Controller_M->Timing.clockTick1)) {
      ++Vel_PI_Controller_M->Timing.clockTickH1;
    }

    Vel_PI_Controller_M->Timing.t[1] = Vel_PI_Controller_M->Timing.clockTick1 *
      Vel_PI_Controller_M->Timing.stepSize1 +
      Vel_PI_Controller_M->Timing.clockTickH1 *
      Vel_PI_Controller_M->Timing.stepSize1 * 4294967296.0;
  }
}

/* Derivatives for root system: '<Root>' */
void Vel_PI_Controller_derivatives(void)
{
  XDot_Vel_PI_Controller_T *_rtXdot;
  _rtXdot = ((XDot_Vel_PI_Controller_T *) Vel_PI_Controller_M->derivs);

  /* Derivatives for TransferFcn: '<Root>/Transfer Fcn' */
  _rtXdot->TransferFcn_CSTATE = Vel_PI_Controller_P.TransferFcn_A *
    Vel_PI_Controller_X.TransferFcn_CSTATE;
  _rtXdot->TransferFcn_CSTATE += Vel_PI_Controller_B.Sum;
}

/* Model initialize function */
void Vel_PI_Controller_initialize(void)
{
  /* Start for S-Function (hil_initialize_block): '<Root>/HIL Initialize' */

  /* S-Function Block: Vel_PI_Controller/HIL Initialize (hil_initialize_block) */
  {
    t_int result;
    t_boolean is_switching;
    result = hil_open("qube_servo3_usb", "0",
                      &Vel_PI_Controller_DW.HILInitialize_Card);
    if (result < 0) {
      msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
        (_rt_error_message));
      rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
      return;
    }

    is_switching = false;
    result = hil_set_card_specific_options
      (Vel_PI_Controller_DW.HILInitialize_Card,
       "deadband_compensation=0.3;pwm_en=0;enc0_velocity=3.0;enc1_velocity=3.0;min_diode_compensation=0.3;max_diode_compensation=1.5",
       125);
    if (result < 0) {
      msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
        (_rt_error_message));
      rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
      return;
    }

    result = hil_watchdog_clear(Vel_PI_Controller_DW.HILInitialize_Card);
    if (result < 0 && result != -QERR_HIL_WATCHDOG_CLEAR) {
      msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
        (_rt_error_message));
      rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
      return;
    }

    if ((Vel_PI_Controller_P.HILInitialize_AIPStart && !is_switching) ||
        (Vel_PI_Controller_P.HILInitialize_AIPEnter && is_switching)) {
      result = hil_set_analog_input_ranges
        (Vel_PI_Controller_DW.HILInitialize_Card,
         &Vel_PI_Controller_P.HILInitialize_AIChannels, 1U,
         &Vel_PI_Controller_P.HILInitialize_AILow,
         &Vel_PI_Controller_P.HILInitialize_AIHigh);
      if (result < 0) {
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
        return;
      }
    }

    if ((Vel_PI_Controller_P.HILInitialize_AOPStart && !is_switching) ||
        (Vel_PI_Controller_P.HILInitialize_AOPEnter && is_switching)) {
      result = hil_set_analog_output_ranges
        (Vel_PI_Controller_DW.HILInitialize_Card,
         &Vel_PI_Controller_P.HILInitialize_AOChannels, 1U,
         &Vel_PI_Controller_P.HILInitialize_AOLow,
         &Vel_PI_Controller_P.HILInitialize_AOHigh);
      if (result < 0) {
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
        return;
      }
    }

    if ((Vel_PI_Controller_P.HILInitialize_AOStart && !is_switching) ||
        (Vel_PI_Controller_P.HILInitialize_AOEnter && is_switching)) {
      result = hil_write_analog(Vel_PI_Controller_DW.HILInitialize_Card,
        &Vel_PI_Controller_P.HILInitialize_AOChannels, 1U,
        &Vel_PI_Controller_P.HILInitialize_AOInitial);
      if (result < 0) {
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
        return;
      }
    }

    if (Vel_PI_Controller_P.HILInitialize_AOReset) {
      result = hil_watchdog_set_analog_expiration_state
        (Vel_PI_Controller_DW.HILInitialize_Card,
         &Vel_PI_Controller_P.HILInitialize_AOChannels, 1U,
         &Vel_PI_Controller_P.HILInitialize_AOWatchdog);
      if (result < 0) {
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
        return;
      }
    }

    result = hil_set_digital_directions(Vel_PI_Controller_DW.HILInitialize_Card,
      NULL, 0U, &Vel_PI_Controller_P.HILInitialize_DOChannels, 1U);
    if (result < 0) {
      msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
        (_rt_error_message));
      rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
      return;
    }

    if ((Vel_PI_Controller_P.HILInitialize_DOStart && !is_switching) ||
        (Vel_PI_Controller_P.HILInitialize_DOEnter && is_switching)) {
      result = hil_write_digital(Vel_PI_Controller_DW.HILInitialize_Card,
        &Vel_PI_Controller_P.HILInitialize_DOChannels, 1U, (t_boolean *)
        &Vel_PI_Controller_P.HILInitialize_DOInitial);
      if (result < 0) {
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
        return;
      }
    }

    if (Vel_PI_Controller_P.HILInitialize_DOReset) {
      result = hil_watchdog_set_digital_expiration_state
        (Vel_PI_Controller_DW.HILInitialize_Card,
         &Vel_PI_Controller_P.HILInitialize_DOChannels, 1U, (const
          t_digital_state *) &Vel_PI_Controller_P.HILInitialize_DOWatchdog);
      if (result < 0) {
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
        return;
      }
    }

    if ((Vel_PI_Controller_P.HILInitialize_EIPStart && !is_switching) ||
        (Vel_PI_Controller_P.HILInitialize_EIPEnter && is_switching)) {
      Vel_PI_Controller_DW.HILInitialize_QuadratureModes[0] =
        Vel_PI_Controller_P.HILInitialize_EIQuadrature;
      Vel_PI_Controller_DW.HILInitialize_QuadratureModes[1] =
        Vel_PI_Controller_P.HILInitialize_EIQuadrature;
      result = hil_set_encoder_quadrature_mode
        (Vel_PI_Controller_DW.HILInitialize_Card,
         Vel_PI_Controller_P.HILInitialize_EIChannels, 2U,
         (t_encoder_quadrature_mode *)
         &Vel_PI_Controller_DW.HILInitialize_QuadratureModes[0]);
      if (result < 0) {
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
        return;
      }
    }

    if ((Vel_PI_Controller_P.HILInitialize_EIStart && !is_switching) ||
        (Vel_PI_Controller_P.HILInitialize_EIEnter && is_switching)) {
      Vel_PI_Controller_DW.HILInitialize_InitialEICounts[0] =
        Vel_PI_Controller_P.HILInitialize_EIInitial;
      Vel_PI_Controller_DW.HILInitialize_InitialEICounts[1] =
        Vel_PI_Controller_P.HILInitialize_EIInitial;
      result = hil_set_encoder_counts(Vel_PI_Controller_DW.HILInitialize_Card,
        Vel_PI_Controller_P.HILInitialize_EIChannels, 2U,
        &Vel_PI_Controller_DW.HILInitialize_InitialEICounts[0]);
      if (result < 0) {
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
        return;
      }
    }

    if ((Vel_PI_Controller_P.HILInitialize_OOStart && !is_switching) ||
        (Vel_PI_Controller_P.HILInitialize_OOEnter && is_switching)) {
      result = hil_write_other(Vel_PI_Controller_DW.HILInitialize_Card,
        Vel_PI_Controller_P.HILInitialize_OOChannels, 3U,
        Vel_PI_Controller_P.HILInitialize_OOInitial);
      if (result < 0) {
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
        return;
      }
    }

    if (Vel_PI_Controller_P.HILInitialize_OOReset) {
      result = hil_watchdog_set_other_expiration_state
        (Vel_PI_Controller_DW.HILInitialize_Card,
         Vel_PI_Controller_P.HILInitialize_OOChannels, 3U,
         Vel_PI_Controller_P.HILInitialize_OOWatchdog);
      if (result < 0) {
        msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
          (_rt_error_message));
        rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
        return;
      }
    }
  }

  /* Start for S-Function (hil_read_timebase_block): '<Root>/HIL Read Timebase' */

  /* S-Function Block: Vel_PI_Controller/HIL Read Timebase (hil_read_timebase_block) */
  {
    t_error result;
    result = hil_task_create_reader(Vel_PI_Controller_DW.HILInitialize_Card,
      Vel_PI_Controller_P.HILReadTimebase_SamplesInBuffer,
      NULL, 0U,
      &Vel_PI_Controller_P.HILReadTimebase_EncoderChannels, 1U,
      NULL, 0U,
      &Vel_PI_Controller_P.HILReadTimebase_OtherChannels, 1U,
      &Vel_PI_Controller_DW.HILReadTimebase_Task);
    if (result >= 0) {
      result = hil_task_set_buffer_overflow_mode
        (Vel_PI_Controller_DW.HILReadTimebase_Task, (t_buffer_overflow_mode)
         (Vel_PI_Controller_P.HILReadTimebase_OverflowMode - 1));
    }

    if (result < 0) {
      msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
        (_rt_error_message));
      rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
    }
  }

  /* Start for FromWorkspace: '<Root>/From Workspace' */
  {
    static real_T pTimeValues0[] = { 0.0, 0.1, 0.2, 0.30000000000000004, 0.4,
      0.5, 0.60000000000000009, 0.70000000000000007, 0.8, 0.9, 1.0, 1.1,
      1.2000000000000002, 1.3, 1.4000000000000001, 1.5, 1.6, 1.7000000000000002,
      1.8, 1.9000000000000001, 2.0, 2.1, 2.2, 2.3000000000000003,
      2.4000000000000004, 2.5, 2.5999999999999996, 2.6999999999999997, 2.8, 2.9,
      3.0, 3.0999999999999996, 3.2, 3.3, 3.4, 3.5, 3.5999999999999996, 3.7, 3.8,
      3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0 } ;

    static real_T pDataValues0[] = { 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0,
      20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0,
      20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0,
      20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0,
      20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0 } ;

    Vel_PI_Controller_DW.FromWorkspace_PWORK.TimePtr = (void *) pTimeValues0;
    Vel_PI_Controller_DW.FromWorkspace_PWORK.DataPtr = (void *) pDataValues0;
    Vel_PI_Controller_DW.FromWorkspace_IWORK.PrevIndex = 0;
  }

  /* InitializeConditions for TransferFcn: '<Root>/Transfer Fcn' */
  Vel_PI_Controller_X.TransferFcn_CSTATE = 0.0;
}

/* Model terminate function */
void Vel_PI_Controller_terminate(void)
{
  /* Terminate for S-Function (hil_initialize_block): '<Root>/HIL Initialize' */

  /* S-Function Block: Vel_PI_Controller/HIL Initialize (hil_initialize_block) */
  {
    t_boolean is_switching;
    t_int result;
    t_uint32 num_final_analog_outputs = 0;
    t_uint32 num_final_digital_outputs = 0;
    t_uint32 num_final_other_outputs = 0;
    hil_task_stop_all(Vel_PI_Controller_DW.HILInitialize_Card);
    hil_monitor_stop_all(Vel_PI_Controller_DW.HILInitialize_Card);
    is_switching = false;
    if ((Vel_PI_Controller_P.HILInitialize_AOTerminate && !is_switching) ||
        (Vel_PI_Controller_P.HILInitialize_AOExit && is_switching)) {
      num_final_analog_outputs = 1U;
    } else {
      num_final_analog_outputs = 0;
    }

    if ((Vel_PI_Controller_P.HILInitialize_DOTerminate && !is_switching) ||
        (Vel_PI_Controller_P.HILInitialize_DOExit && is_switching)) {
      num_final_digital_outputs = 1U;
    } else {
      num_final_digital_outputs = 0;
    }

    if ((Vel_PI_Controller_P.HILInitialize_OOTerminate && !is_switching) ||
        (Vel_PI_Controller_P.HILInitialize_OOExit && is_switching)) {
      num_final_other_outputs = 3U;
    } else {
      num_final_other_outputs = 0;
    }

    if (0
        || num_final_analog_outputs > 0
        || num_final_digital_outputs > 0
        || num_final_other_outputs > 0
        ) {
      /* Attempt to write the final outputs atomically (due to firmware issue in old Q2-USB). Otherwise write channels individually */
      result = hil_write(Vel_PI_Controller_DW.HILInitialize_Card
                         , &Vel_PI_Controller_P.HILInitialize_AOChannels,
                         num_final_analog_outputs
                         , NULL, 0
                         , &Vel_PI_Controller_P.HILInitialize_DOChannels,
                         num_final_digital_outputs
                         , Vel_PI_Controller_P.HILInitialize_OOChannels,
                         num_final_other_outputs
                         , &Vel_PI_Controller_P.HILInitialize_AOFinal
                         , NULL
                         , (t_boolean *)
                         &Vel_PI_Controller_P.HILInitialize_DOFinal
                         , Vel_PI_Controller_P.HILInitialize_OOFinal
                         );
      if (result == -QERR_HIL_WRITE_NOT_SUPPORTED) {
        t_error local_result;
        result = 0;

        /* The hil_write operation is not supported by this card. Write final outputs for each channel type */
        if (num_final_analog_outputs > 0) {
          local_result = hil_write_analog
            (Vel_PI_Controller_DW.HILInitialize_Card,
             &Vel_PI_Controller_P.HILInitialize_AOChannels,
             num_final_analog_outputs,
             &Vel_PI_Controller_P.HILInitialize_AOFinal);
          if (local_result < 0) {
            result = local_result;
          }
        }

        if (num_final_digital_outputs > 0) {
          local_result = hil_write_digital
            (Vel_PI_Controller_DW.HILInitialize_Card,
             &Vel_PI_Controller_P.HILInitialize_DOChannels,
             num_final_digital_outputs, (t_boolean *)
             &Vel_PI_Controller_P.HILInitialize_DOFinal);
          if (local_result < 0) {
            result = local_result;
          }
        }

        if (num_final_other_outputs > 0) {
          local_result = hil_write_other(Vel_PI_Controller_DW.HILInitialize_Card,
            Vel_PI_Controller_P.HILInitialize_OOChannels,
            num_final_other_outputs, Vel_PI_Controller_P.HILInitialize_OOFinal);
          if (local_result < 0) {
            result = local_result;
          }
        }

        if (result < 0) {
          msg_get_error_messageA(NULL, result, _rt_error_message, sizeof
            (_rt_error_message));
          rtmSetErrorStatus(Vel_PI_Controller_M, _rt_error_message);
        }
      }
    }

    hil_task_delete_all(Vel_PI_Controller_DW.HILInitialize_Card);
    hil_monitor_delete_all(Vel_PI_Controller_DW.HILInitialize_Card);
    hil_close(Vel_PI_Controller_DW.HILInitialize_Card);
    Vel_PI_Controller_DW.HILInitialize_Card = NULL;
  }
}

/*========================================================================*
 * Start of Classic call interface                                        *
 *========================================================================*/

/* Solver interface called by GRT_Main */
#ifndef USE_GENERATED_SOLVER

void rt_ODECreateIntegrationData(RTWSolverInfo *si)
{
  UNUSED_PARAMETER(si);
  return;
}                                      /* do nothing */

void rt_ODEDestroyIntegrationData(RTWSolverInfo *si)
{
  UNUSED_PARAMETER(si);
  return;
}                                      /* do nothing */

void rt_ODEUpdateContinuousStates(RTWSolverInfo *si)
{
  UNUSED_PARAMETER(si);
  return;
}                                      /* do nothing */

#endif

void MdlOutputs(int_T tid)
{
  Vel_PI_Controller_output();
  UNUSED_PARAMETER(tid);
}

void MdlUpdate(int_T tid)
{
  Vel_PI_Controller_update();
  UNUSED_PARAMETER(tid);
}

void MdlInitializeSizes(void)
{
}

void MdlInitializeSampleTimes(void)
{
}

void MdlInitialize(void)
{
}

void MdlStart(void)
{
  Vel_PI_Controller_initialize();
}

void MdlTerminate(void)
{
  Vel_PI_Controller_terminate();
}

/* Registration function */
RT_MODEL_Vel_PI_Controller_T *Vel_PI_Controller(void)
{
  /* Registration code */

  /* initialize real-time model */
  (void) memset((void *)Vel_PI_Controller_M, 0,
                sizeof(RT_MODEL_Vel_PI_Controller_T));

  {
    /* Setup solver object */
    rtsiSetSimTimeStepPtr(&Vel_PI_Controller_M->solverInfo,
                          &Vel_PI_Controller_M->Timing.simTimeStep);
    rtsiSetTPtr(&Vel_PI_Controller_M->solverInfo, &rtmGetTPtr
                (Vel_PI_Controller_M));
    rtsiSetStepSizePtr(&Vel_PI_Controller_M->solverInfo,
                       &Vel_PI_Controller_M->Timing.stepSize0);
    rtsiSetdXPtr(&Vel_PI_Controller_M->solverInfo, &Vel_PI_Controller_M->derivs);
    rtsiSetContStatesPtr(&Vel_PI_Controller_M->solverInfo, (real_T **)
                         &Vel_PI_Controller_M->contStates);
    rtsiSetNumContStatesPtr(&Vel_PI_Controller_M->solverInfo,
      &Vel_PI_Controller_M->Sizes.numContStates);
    rtsiSetNumPeriodicContStatesPtr(&Vel_PI_Controller_M->solverInfo,
      &Vel_PI_Controller_M->Sizes.numPeriodicContStates);
    rtsiSetPeriodicContStateIndicesPtr(&Vel_PI_Controller_M->solverInfo,
      &Vel_PI_Controller_M->periodicContStateIndices);
    rtsiSetPeriodicContStateRangesPtr(&Vel_PI_Controller_M->solverInfo,
      &Vel_PI_Controller_M->periodicContStateRanges);
    rtsiSetContStateDisabledPtr(&Vel_PI_Controller_M->solverInfo, (boolean_T**)
      &Vel_PI_Controller_M->contStateDisabled);
    rtsiSetErrorStatusPtr(&Vel_PI_Controller_M->solverInfo, (&rtmGetErrorStatus
      (Vel_PI_Controller_M)));
    rtsiSetRTModelPtr(&Vel_PI_Controller_M->solverInfo, Vel_PI_Controller_M);
  }

  rtsiSetSimTimeStep(&Vel_PI_Controller_M->solverInfo, MAJOR_TIME_STEP);
  rtsiSetIsMinorTimeStepWithModeChange(&Vel_PI_Controller_M->solverInfo, false);
  rtsiSetIsContModeFrozen(&Vel_PI_Controller_M->solverInfo, false);
  Vel_PI_Controller_M->intgData.y = Vel_PI_Controller_M->odeY;
  Vel_PI_Controller_M->intgData.f[0] = Vel_PI_Controller_M->odeF[0];
  Vel_PI_Controller_M->intgData.f[1] = Vel_PI_Controller_M->odeF[1];
  Vel_PI_Controller_M->intgData.f[2] = Vel_PI_Controller_M->odeF[2];
  Vel_PI_Controller_M->contStates = ((real_T *) &Vel_PI_Controller_X);
  Vel_PI_Controller_M->contStateDisabled = ((boolean_T *)
    &Vel_PI_Controller_XDis);
  Vel_PI_Controller_M->Timing.tStart = (0.0);
  rtsiSetSolverData(&Vel_PI_Controller_M->solverInfo, (void *)
                    &Vel_PI_Controller_M->intgData);
  rtsiSetSolverName(&Vel_PI_Controller_M->solverInfo,"ode3");

  /* Initialize timing info */
  {
    int_T *mdlTsMap = Vel_PI_Controller_M->Timing.sampleTimeTaskIDArray;
    mdlTsMap[0] = 0;
    mdlTsMap[1] = 1;
    Vel_PI_Controller_M->Timing.sampleTimeTaskIDPtr = (&mdlTsMap[0]);
    Vel_PI_Controller_M->Timing.sampleTimes =
      (&Vel_PI_Controller_M->Timing.sampleTimesArray[0]);
    Vel_PI_Controller_M->Timing.offsetTimes =
      (&Vel_PI_Controller_M->Timing.offsetTimesArray[0]);

    /* task periods */
    Vel_PI_Controller_M->Timing.sampleTimes[0] = (0.0);
    Vel_PI_Controller_M->Timing.sampleTimes[1] = (0.002);

    /* task offsets */
    Vel_PI_Controller_M->Timing.offsetTimes[0] = (0.0);
    Vel_PI_Controller_M->Timing.offsetTimes[1] = (0.0);
  }

  rtmSetTPtr(Vel_PI_Controller_M, &Vel_PI_Controller_M->Timing.tArray[0]);

  {
    int_T *mdlSampleHits = Vel_PI_Controller_M->Timing.sampleHitArray;
    mdlSampleHits[0] = 1;
    mdlSampleHits[1] = 1;
    Vel_PI_Controller_M->Timing.sampleHits = (&mdlSampleHits[0]);
  }

  rtmSetTFinal(Vel_PI_Controller_M, 5.0);
  Vel_PI_Controller_M->Timing.stepSize0 = 0.002;
  Vel_PI_Controller_M->Timing.stepSize1 = 0.002;

  /* External mode info */
  Vel_PI_Controller_M->Sizes.checksums[0] = (4064660136U);
  Vel_PI_Controller_M->Sizes.checksums[1] = (4163518053U);
  Vel_PI_Controller_M->Sizes.checksums[2] = (2576824875U);
  Vel_PI_Controller_M->Sizes.checksums[3] = (1340499957U);

  {
    static const sysRanDType rtAlwaysEnabled = SUBSYS_RAN_BC_ENABLE;
    static RTWExtModeInfo rt_ExtModeInfo;
    static const sysRanDType *systemRan[1];
    Vel_PI_Controller_M->extModeInfo = (&rt_ExtModeInfo);
    rteiSetSubSystemActiveVectorAddresses(&rt_ExtModeInfo, systemRan);
    systemRan[0] = &rtAlwaysEnabled;
    rteiSetModelMappingInfoPtr(Vel_PI_Controller_M->extModeInfo,
      &Vel_PI_Controller_M->SpecialInfo.mappingInfo);
    rteiSetChecksumsPtr(Vel_PI_Controller_M->extModeInfo,
                        Vel_PI_Controller_M->Sizes.checksums);
    rteiSetTPtr(Vel_PI_Controller_M->extModeInfo, rtmGetTPtr(Vel_PI_Controller_M));
  }

  Vel_PI_Controller_M->solverInfoPtr = (&Vel_PI_Controller_M->solverInfo);
  Vel_PI_Controller_M->Timing.stepSize = (0.002);
  rtsiSetFixedStepSize(&Vel_PI_Controller_M->solverInfo, 0.002);
  rtsiSetSolverMode(&Vel_PI_Controller_M->solverInfo, SOLVER_MODE_SINGLETASKING);

  /* block I/O */
  Vel_PI_Controller_M->blockIO = ((void *) &Vel_PI_Controller_B);
  (void) memset(((void *) &Vel_PI_Controller_B), 0,
                sizeof(B_Vel_PI_Controller_T));

  /* parameters */
  Vel_PI_Controller_M->defaultParam = ((real_T *)&Vel_PI_Controller_P);

  /* states (continuous) */
  {
    real_T *x = (real_T *) &Vel_PI_Controller_X;
    Vel_PI_Controller_M->contStates = (x);
    (void) memset((void *)&Vel_PI_Controller_X, 0,
                  sizeof(X_Vel_PI_Controller_T));
  }

  /* disabled states */
  {
    boolean_T *xdis = (boolean_T *) &Vel_PI_Controller_XDis;
    Vel_PI_Controller_M->contStateDisabled = (xdis);
    (void) memset((void *)&Vel_PI_Controller_XDis, 0,
                  sizeof(XDis_Vel_PI_Controller_T));
  }

  /* states (dwork) */
  Vel_PI_Controller_M->dwork = ((void *) &Vel_PI_Controller_DW);
  (void) memset((void *)&Vel_PI_Controller_DW, 0,
                sizeof(DW_Vel_PI_Controller_T));

  /* data type transition information */
  {
    static DataTypeTransInfo dtInfo;
    (void) memset((char_T *) &dtInfo, 0,
                  sizeof(dtInfo));
    Vel_PI_Controller_M->SpecialInfo.mappingInfo = (&dtInfo);
    dtInfo.numDataTypes = 21;
    dtInfo.dataTypeSizes = &rtDataTypeSizes[0];
    dtInfo.dataTypeNames = &rtDataTypeNames[0];

    /* Block I/O transition table */
    dtInfo.BTransTable = &rtBTransTable;

    /* Parameters transition table */
    dtInfo.PTransTable = &rtPTransTable;
  }

  /* Initialize Sizes */
  Vel_PI_Controller_M->Sizes.numContStates = (1);/* Number of continuous states */
  Vel_PI_Controller_M->Sizes.numPeriodicContStates = (0);
                                      /* Number of periodic continuous states */
  Vel_PI_Controller_M->Sizes.numY = (0);/* Number of model outputs */
  Vel_PI_Controller_M->Sizes.numU = (0);/* Number of model inputs */
  Vel_PI_Controller_M->Sizes.sysDirFeedThru = (0);/* The model is not direct feedthrough */
  Vel_PI_Controller_M->Sizes.numSampTimes = (2);/* Number of sample times */
  Vel_PI_Controller_M->Sizes.numBlocks = (15);/* Number of blocks */
  Vel_PI_Controller_M->Sizes.numBlockIO = (5);/* Number of block outputs */
  Vel_PI_Controller_M->Sizes.numBlockPrms = (91);/* Sum of parameter "widths" */
  return Vel_PI_Controller_M;
}

/*========================================================================*
 * End of Classic call interface                                          *
 *========================================================================*/
