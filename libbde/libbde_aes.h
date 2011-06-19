/*
 * AES encryption functions
 *
 * Copyright (C) 2011, Joachim Metz <jbmetz@users.sourceforge.net>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This software is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public License
 * along with this software.  If not, see <http://www.gnu.org/licenses/>.
 */

#if !defined( _LIBBDE_AES_H )
#define _LIBBDE_AES_H

#include <common.h>
#include <types.h>

#include <liberror.h>

#if defined( WINAPI )
#include <wincrypt.h>

#elif defined( HAVE_LIBCRYPTO ) && defined( HAVE_OPENSSL_EVP_H )
#include <openssl/evp.h>

#elif defined( HAVE_LIBCRYPTO ) && defined( HAVE_OPENSSL_AES_H )
#include <openssl/aes.h>

#endif

#if defined( __cplusplus )
extern "C" {
#endif

enum LIBBDE_AES_CRYPT_MODES
{
	LIBBDE_AES_CRYPT_MODE_ENCRYPT		= 0,
	LIBBDE_AES_CRYPT_MODE_DECRYPT		= 1
};

#if defined( WINAPI )
typedef struct libbde_aes_context libbde_aes_context_t;

struct libbde_aes_context
{
        HCRYPTPROV crypt_provider;
        HCRYPTHASH hash;
};

#elif defined( HAVE_LIBCRYPTO ) && defined( HAVE_OPENSSL_EVP_H )
typedef EVP_MD_CTX libbde_aes_context_t;

#elif defined( HAVE_LIBCRYPTO ) && defined( HAVE_OPENSSL_AES_H )
typedef struct libbde_aes_context libbde_aes_context_t;

struct libbde_aes_context
{
        AES_KEY key;
};

#else
typedef struct libbde_aes_context libbde_aes_context_t;

struct libbde_aes_context
{
	/* The number of round keys
	 */
	uint8_t number_of_round_keys;

	/* The round keys
	 */
	uint32_t *round_keys;

	/* The round keys data
	 */
	uint32_t round_keys_data[ 68 ];

/* TODO code clean up for fallback */
	int nr;
	unsigned long *rk;
	unsigned long buf[68];
};

#endif

int libbde_aes_initialize(
     libbde_aes_context_t *context,
     liberror_error_t **error );

int libbde_aes_finalize(
     libbde_aes_context_t *context,
     liberror_error_t **error );

int libbde_aes_set_decryption_key(
     libbde_aes_context_t *context,
     const uint8_t *key,
     size_t bit_size,
     liberror_error_t **error );

int libbde_aes_set_encryption_key(
     libbde_aes_context_t *context,
     const uint8_t *key,
     size_t bit_size,
     liberror_error_t **error );

int libbde_aes_ccm_crypt(
     libbde_aes_context_t *context,
     int mode,
     const uint8_t *initialization_vector,
     size_t initialization_vector_size,
     const uint8_t *input_data,
     size_t input_data_size,
     uint8_t *output_data,
     size_t output_data_size,
     liberror_error_t **error );

int libbde_aes_ecb_crypt(
     libbde_aes_context_t *context,
     int mode,
     const uint8_t *input_data,
     size_t input_data_size,
     uint8_t *output_data,
     size_t output_data_size,
     liberror_error_t **error );

int libbde_aes_cbc_crypt(
     libbde_aes_context_t *context,
     int mode,
     int length,
     unsigned char iv[16],
     const uint8_t *input_data,
     size_t input_data_size,
     uint8_t *output_data,
     size_t output_data_size,
     liberror_error_t **error );

int libbde_aes_cfb_crypt(
     libbde_aes_context_t *context,
     int mode,
     uint8_t initialization_vector[ 16 ],
     size_t *initialization_vector_index,
     const uint8_t *input_data,
     size_t input_data_size,
     uint8_t *output_data,
     size_t output_data_size,
     liberror_error_t **error );

int libbde_aes_self_test(
     int verbose );

#ifdef __cplusplus
}
#endif

#endif
