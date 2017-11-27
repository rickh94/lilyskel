\version "{{ piece.version }}"
{%- if piece.language %}
\language "{{ piece.language }}"
{%- endif %}

% includes.ily - included files for {{ piece.headers.title }}

#(ly:set-option 'relative-includes #t)
% user defined includes
{%- for item in extra_includes %}
\include "{{ item }}"
{%- endfor %}

% auto-generated includes. These are needed for proper rendering.
{%- for item in includepaths %}
\include "{{ item }}"
{%- endfor %}

{# vim: se ft=lilypond: #}
