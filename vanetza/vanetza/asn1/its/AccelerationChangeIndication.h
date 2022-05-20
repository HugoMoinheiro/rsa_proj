/*
 * Generated by asn1c-0.9.29 (http://lionet.info/asn1c)
 * From ASN.1 module "VAM-PDU-Descriptions"
 * 	found in "asn1/TS103300-3v211-VAM.asn"
 * 	`asn1c -fcompound-names -fincludes-quoted -no-gen-example -R`
 */

#ifndef	_AccelerationChangeIndication_H_
#define	_AccelerationChangeIndication_H_


#include "asn_application.h"

/* Including external dependencies */
#include "AccelOrDecel.h"
#include "ActionDeltaTime.h"
#include "constr_SEQUENCE.h"

#ifdef __cplusplus
extern "C" {
#endif

/* AccelerationChangeIndication */
typedef struct AccelerationChangeIndication {
	AccelOrDecel_t	 accelOrDecel;
	ActionDeltaTime_t	 actionDeltaTime;
	/*
	 * This type is extensible,
	 * possible extensions are below.
	 */
	
	/* Context for parsing across buffer boundaries */
	asn_struct_ctx_t _asn_ctx;
} AccelerationChangeIndication_t;

/* Implementation */
extern asn_TYPE_descriptor_t asn_DEF_AccelerationChangeIndication;
extern asn_SEQUENCE_specifics_t asn_SPC_AccelerationChangeIndication_specs_1;
extern asn_TYPE_member_t asn_MBR_AccelerationChangeIndication_1[2];

#ifdef __cplusplus
}
#endif

#endif	/* _AccelerationChangeIndication_H_ */
#include "asn_internal.h"
