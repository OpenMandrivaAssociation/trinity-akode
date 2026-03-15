%bcond clang 1
%bcond jack 1
%bcond libsamplerate 1
%bcond pulseaudio 1
%bcond libmad 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg akode

%define libname %mklibname %{tde_pkg}
%define devname %mklibname %{tde_pkg} -d

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity

Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	2.0.2
Release:	%{?tde_version:%{tde_version}_}5
Summary: 	Audio-decoding framework
Group: 		System Environment/Libraries
URL:		http://www.kde-apps.org/content/show.php?content=30375
#URL:		http://carewolf.com/akode/  

License:	GPLv2+

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}.tar.xz

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
BuildOption:  -DWITH_MPEG_DECODER=%{!?with_libmad:OFF}%{?with_libmad:ON}
BuildOption:  -DWITH_JACK_SINK=%{!?with_jack:OFF}%{?with_jack:ON}
BuildOption:  -DWITH_PULSE_SINK=%{!?with_pulseaudio:OFF}%{?with_pulseaudio:ON}

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:  gcc-c++}

BuildRequires:	libtool

# TQT support
BuildRequires:	pkgconfig(tqt)
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

##########

%package -n %{devname}
Summary: Headers for developing programs that will use %{name} 
Group:   Development/Libraries
Requires: %{name} = %{EVRD}
%{?with_jack:Requires: %{libname}_jack_sink = %{EVRD}}
%{?with_pulseaudio:Requires: %{libname}_pulse_sink = %{EVRD}}
%{?with_libsamplerate:Requires: %{libname}_src_resampler = %{EVRD}}
%{?with_libmad:Requires: %{libname}_mpeg_decoder  = %{EVRD}}
Requires: pkgconfig

%description -n %{devname}
This package contains the development files for Akode.
It is needed if you intend to build an application linked against Akode.

%files -n %{devname}
%defattr(-,root,root,-)
%{_bindir}/akode-config
%{_includedir}/*
%{_libdir}/libakode.la
%{_libdir}/libakode.so
%{_libdir}/pkgconfig/akode.pc


##########
%package -n %{libname}_jack_sink
Summary: Jack audio output backend for %{name}
Group:   Development/Libraries

Requires: %{name} = %{EVRD}

%description -n %{libname}_jack_sink
This package contains the Jack audio output backend for Akode.

%files -n %{libname}_jack_sink
%defattr(-,root,root,-)
%{_libdir}/libakode_jack_sink.la
%{_libdir}/libakode_jack_sink.so


##########

%package -n %{libname}_pulse_sink
Summary: Pulseaudio output backend for %{name}
Group:   Development/Libraries

Requires: %{name} = %{EVRD}

%description -n %{libname}_pulse_sink
This package contains the pulseaudio backend for Akode.
Recommended for network transparent audio.

%files -n %{libname}_pulse_sink
%defattr(-,root,root,-)
%{_libdir}/libakode_pulse_sink.la
%{_libdir}/libakode_pulse_sink.so


##########

# Packaged separately to keep main/core %{akode} package LGPL-clean.
%package -n %{libname}_src_resampler
Summary: Resampler based on libsamplerate for %{name}
Group:   Development/Libraries

Requires: %{name} = %{EVRD}

%description -n %{libname}_src_resampler 
This package contains the samplerate decoder for Akode.

%files -n %{libname}_src_resampler
%defattr(-,root,root,-)
%{_libdir}/libakode_src_resampler.la
%{_libdir}/libakode_src_resampler.so


##########

%package -n %{libname}_mpeg_decoder
Summary: Decoder based on libmad for %{name}
Group:   Development/Libraries

Requires: %{name} = %{EVRD}

%description -n %{libname}_mpeg_decoder 
This package contains the mad decoder for Akode.

%files -n %{libname}_mpeg_decoder
%defattr(-,root,root,-)
%{_libdir}/libakode_mpeg_decoder.la
%{_libdir}/libakode_mpeg_decoder.so

%install -a
# rpmdocs
for file in AUTHORS COPYING NEWS README TODO ; do
  test -s  "$file" && install -p -m644 -D "$file" "rpmdocs/$file"
done

