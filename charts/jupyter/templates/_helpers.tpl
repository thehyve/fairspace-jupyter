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

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "jupyter.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "jupyter.labels" -}}
chart: {{ include "jupyter.chart" . }}
release: {{ .Release.Name }}
heritage: {{ .Release.Service }}
helm.sh/chart: {{ include "jupyter.chart" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/release-name: {{ .Release.Name }}
{{- end }}
