{{/*
Create a name for the tls secret for jupyter-workspace
*/}}
{{- define "tlsSecretName" -}}
{{- if .Values.ingress.tls.secretNameOverride -}}
{{- .Values.ingress.tls.secretNameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- printf "tls-%s" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "tls-%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "jupyter.url" -}}
{{- if .Values.ingress.tls.enabled -}}
https://{{ .Values.ingress.domain }}
{{- else -}}
http://{{ .Values.ingress.domain }}
{{- end -}}
{{- end -}}

