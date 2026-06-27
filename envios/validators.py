from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


def validar_peso_positivo(value):
    if value <= 0:
        raise ValidationError('El peso debe ser estrictamente mayor a 0 kg.')


def validar_telefono_peru(value):
    telefono_limpio = re.sub(r'[\s\-\(\)]', '', str(value))
    if not re.match(r'^(9\d{8}|\+519\d{8})$', telefono_limpio):
        raise ValidationError(
            'Número telefónico inválido. Debe ser un número móvil peruano (9 dígitos iniciando con 9).'
        )


def validar_codigo_encomienda(value):
    if not re.match(r'^ENC-\d{6}-[A-Z]{2}$', value):
        raise ValidationError(
            'Código de encomienda inválido. Formato requerido: ENC-XXXXXX-XX (ejemplo: ENC-000001-LM)'
        )


def validar_documento_dni(value):
    if not re.match(r'^\d{8}$', str(value)):
        raise ValidationError('DNI inválido. Debe contener exactamente 8 dígitos numéricos.')


def validar_documento_ruc(value):
    if not re.match(r'^\d{11}$', str(value)):
        raise ValidationError('RUC inválido. Debe contener exactamente 11 dígitos numéricos.')
