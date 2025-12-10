%bcond clang 1
%bcond jack 1
%bcond libsamplerate 1
%bcond pulseaudio 1
%bcond libmad 1

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg akode
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define libakode %{_lib}akode

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity

Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	2.0.2
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary: 	Audio-decoding framework
Group: 		System Environment/Libraries
URL:		http://www.kde-apps.org/content/show.php?content=30375
#URL:		http://carewolf.com/akode/  

License:	GPLv2+

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

Prefix:		%{tde_prefix}

BuildSystem:  cmake
BuildOption:  -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:  -DWITH_ALL_OPTIONS=ON
BuildOption:  -DWITH_LIBLTDL=OFF
BuildOption:  -DWITH_ALSA_SINK=ON
BuildOption:  -DWITH_OSS_SINK=ON
BuildOption:  -DWITH_SUN_SINK=OFF
BuildOption:  -DWITH_FFMPEG_DECODER=OFF
BuildOption:  -DWITH_MPC_DECODER=ON
BuildOption:  -DWITH_SRC_RESAMPLER=ON
BuildOption:  -DWITH_XIPH_DECODER=ON
%{!?with_libmad:BuildOption:  -DWITH_MPEG_DECODER=OFF}
%{?with_libmad:BuildOption:  -DWITH_MPEG_DECODER=ON}
%{!?with_jack:BuildOption:  -DWITH_JACK_SINK=OFF} 
%{?with_jack:BuildOption:  -DWITH_JACK_SINK=ON}
%{!?with_pulseaudio:BuildOption:  -DWITH_PULSE_SINK=OFF} 
%{?with_pulseaudio:BuildOption:  -DWITH_PULSE_SINK=ON}

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:  gcc-c++}

BuildRequires:	libtool

# TQT support
BuildRequires:	libtqt4-devel
BuildRequires:	trinity-filesystem >= %{tde_version}

# FLAC support
BuildRequires:  pkgconfig(flac)

# JACK support
%{?with_jack:BuildRequires:  pkgconfig(jack)}

# SAMPLERATE support
%{?with_libsamplerate:BuildRequires:  pkgconfig(samplerate)}

# PULSEAUDIO support
%{?with_pulseaudio:BuildRequires:  pkgconfig(libpulse)}

# MAD support
%{?with_libmad:BuildRequires:  pkgconfig(mad)}

# ALSA support
BuildRequires:  pkgconfig(alsa)

# VORBIS support
BuildRequires:  pkgconfig(vorbis)

BuildRequires:  pkgconfig(speex)


%description
aKode is a simple audio-decoding frame-work that provides a uniform
interface to decode the most common audio-formats. It also has a direct
playback option for a number of audio-outputs.

aKode currently has the following decoder plugins:
* mpc: Decodes musepack aka mpc audio.
* xiph: Decodes FLAC, Ogg/FLAC, Speex and Ogg Vorbis audio. 

aKode also has the following audio outputs:
* alsa: Outputs to ALSA (dmix is recommended).
* jack
* pulseaudio

%files
%defattr(-,root,root,-)
%doc rpmdocs/* 
%{_bindir}/akodeplay
%{_libdir}/libakode.so.*
%{_libdir}/libakode_alsa_sink.la
%{_libdir}/libakode_alsa_sink.so
%{_libdir}/libakode_mpc_decoder.la
%{_libdir}/libakode_mpc_decoder.so
%{_libdir}/libakode_oss_sink.la
%{_libdir}/libakode_oss_sink.so
%{_libdir}/libakode_xiph_decoder.la
%{_libdir}/libakode_xiph_decoder.so

%post
/sbin/ldconfig

%postun 
/sbin/ldconfig

##########

%package devel
Summary: Headers for developing programs that will use %{name} 
Group:   Development/Libraries
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%{?with_jack:Requires: %{libakode}_jack_sink = %{?epoch:%{epoch}:}%{version}-%{release}}
%{?with_pulseaudio:Requires: %{libakode}_pulse_sink = %{?epoch:%{epoch}:}%{version}-%{release}}
%{?with_libsamplerate:Requires: %{libakode}_src_resampler = %{?epoch:%{epoch}:}%{version}-%{release}}
%{?with_libmad:Requires: %{libakode}_mpeg_decoder  = %{?epoch:%{epoch}:}%{version}-%{release}}
Requires: pkgconfig

%description devel
This package contains the development files for Akode.
It is needed if you intend to build an application linked against Akode.

%files devel
%defattr(-,root,root,-)
%{_bindir}/akode-config
%{_includedir}/*
%{_libdir}/libakode.la
%{_libdir}/libakode.so
%{_libdir}/pkgconfig/akode.pc

%post devel
/sbin/ldconfig

%postun devel
/sbin/ldconfig

##########
%package -n %{libakode}_jack_sink
Summary: Jack audio output backend for %{name}
Group:   Development/Libraries
Provides: libakode_jack_sink = %{version}-%{release}
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libakode}_jack_sink
This package contains the Jack audio output backend for Akode.

%files -n %{libakode}_jack_sink
%defattr(-,root,root,-)
%{_libdir}/libakode_jack_sink.la
%{_libdir}/libakode_jack_sink.so

%post -n %{libakode}_jack_sink
/sbin/ldconfig

%postun -n %{libakode}_jack_sink
/sbin/ldconfig

##########

%package -n %{libakode}_pulse_sink
Summary: Pulseaudio output backend for %{name}
Group:   Development/Libraries
Provides: libakode_pulse_sink = %{version}-%{release}
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libakode}_pulse_sink
This package contains the pulseaudio backend for Akode.
Recommended for network transparent audio.

%files -n %{libakode}_pulse_sink
%defattr(-,root,root,-)
%{_libdir}/libakode_pulse_sink.la
%{_libdir}/libakode_pulse_sink.so

%post -n %{libakode}_pulse_sink
/sbin/ldconfig

%postun -n %{libakode}_pulse_sink
/sbin/ldconfig

##########

# Packaged separately to keep main/core %{akode} package LGPL-clean.
%package -n %{libakode}_src_resampler
Summary: Resampler based on libsamplerate for %{name}
Group:   Development/Libraries
Provides: libakode_src_resampler = %{version}-%{release}
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libakode}_src_resampler 
This package contains the samplerate decoder for Akode.

%files -n %{libakode}_src_resampler
%defattr(-,root,root,-)
%{_libdir}/libakode_src_resampler.la
%{_libdir}/libakode_src_resampler.so

%post -n %{libakode}_src_resampler
/sbin/ldconfig

%postun -n %{libakode}_src_resampler 
/sbin/ldconfig

##########

%package -n %{libakode}_mpeg_decoder
Summary: Decoder based on libmad for %{name}
Group:   Development/Libraries
Provides: libakode_mpeg_decoder = %{version}-%{release}
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libakode}_mpeg_decoder 
This package contains the mad decoder for Akode.

%files -n %{libakode}_mpeg_decoder
%defattr(-,root,root,-)
%{_libdir}/libakode_mpeg_decoder.la
%{_libdir}/libakode_mpeg_decoder.so

%post -n %{libakode}_mpeg_decoder
/sbin/ldconfig

%postun -n %{libakode}_mpeg_decoder 
/sbin/ldconfig


%install -a
# rpmdocs
for file in AUTHORS COPYING NEWS README TODO ; do
  test -s  "$file" && install -p -m644 -D "$file" "rpmdocs/$file"
done

