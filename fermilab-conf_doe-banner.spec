Name:		fermilab-conf_doe-banner

Version:	1.0
Release:	5%{?dist}
Summary:	Includes the FNAL approved text for the DOE notice of usage

Group:		Fermilab
License:	MIT
URL:		https://github.com/fermilab-context-rpms/fermilab-conf_doe-banner

Source0:	doe_banner_80_char.txt
Source1:	doe_banner_raw.txt
Source2:	doe_banner_oneline.txt
Source3:	doe_banner_html.txt

Requires:	filesystem system-release
BuildArch:	noarch

# This top level package doesn't require its subpackages

%description
The DOE requests that we publish a login banner on all systems so that
people understand their rights and restrictions on the systems.

Requirement from: CS-doc-5536-v1

%package cockpit
Summary:	FNAL approved text for the DOE notice in cockpit
Group:		Fermilab
Requires:	%{name} >= %{version}-%{release}
Requires(pre):	augeas coreutils policycoreutils
Requires(preun):	augeas coreutils policycoreutils

%description cockpit
The DOE requests that we publish a login banner on all systems so that
people understand their rights and restrictions on the systems.

Requirement from: CS-doc-5536-v1

%package console
Summary:	FNAL approved text for the DOE notice on console
Group:		Fermilab
Requires:	%{name} >= %{version}-%{release}

%if 0%{?rhel} >= 9 || 0%{?fedora} >= 31
# util-linux-core provides agetty
Requires:	util-linux-core >= 2.35
Requires:	pam >= 1.3.1
%else
# the 'setup' rpm provides /etc/motd
#    which we are about to change out.
# the 'system-release' rpm provides /etc/issue
#    which we are about to change out.
Requires:	system-release
Requires(post):	setup coreutils policycoreutils
Requires(postun):	coreutils policycoreutils
%endif

%description console
The DOE requests that we publish a login banner on all systems so that
people understand their rights and restrictions on the systems.

Requirement from: CS-doc-5536-v1

%package login-screen
Summary:	FNAL approved text for the DOE notice within GUI login
Group:		Fermilab
Requires:	%{name} >= %{version}-%{release}

# Top level sub-package should require software specific packages
Requires:	%{name}-cockpit >= %{version}-%{release}
Requires:	%{name}-gdm >= %{version}-%{release}

%description login-screen
The DOE requests that we publish a login banner on all systems so that
people understand their rights and restrictions on the systems.

Requirement from: CS-doc-5536-v1

%package gdm
Summary:        FNAL approved text for the DOE notice within GUI login
Requires:	%{name} >= %{version}-%{release}
Group:          Fermilab
Requires(post):	dconf
Requires(pre):	dconf
Conflicts:	gdm < 3.8

%description gdm
The DOE requests that we publish a login banner on all systems so that
people understand their rights and restrictions on the systems.

Requirement from: CS-doc-5536-v1


%prep

%build

%install

# base package
%{__install} -D %{SOURCE0} %{buildroot}/%{_datarootdir}/%{name}/doe_banner_80_char.txt
%{__install} -D %{SOURCE1} %{buildroot}/%{_datarootdir}/%{name}/doe_banner_raw.txt
%{__install} -D %{SOURCE2} %{buildroot}/%{_datarootdir}/%{name}/doe_banner_oneline.txt
%{__install} -D %{SOURCE2} %{buildroot}/%{_datarootdir}/%{name}/doe_banner_html.txt

# console
%if 0%{?rhel} >= 9 || 0%{?fedora} >= 31
%{__mkdir_p} %{buildroot}/etc/issue.d/
ln -s %{_datarootdir}/%{name}/doe_banner_80_char.txt %{buildroot}/etc/issue.d/doe_banner_80_char.issue
%{__mkdir_p} %{buildroot}/etc/motd.d/
ln -s %{_datarootdir}/%{name}/doe_banner_80_char.txt %{buildroot}/etc/motd.d/doe_banner_80_char
%endif

# GDM
%{__mkdir_p} %{buildroot}/etc/dconf/db/distro.d/locks
echo "### THIS FILE IS MANAGED BY fermilab-conf_doe-banner-gdm ###" > %{buildroot}/etc/dconf/db/distro.d/locks/20-login-banner
echo "###  YOUR CHANGES HERE WILL BE REVERTED BY THIS PACAKGE  ###" >> %{buildroot}/etc/dconf/db/distro.d/locks/20-login-banner
echo "/org/gnome/login-screen/banner-message-text" >> %{buildroot}/etc/dconf/db/distro.d/locks/20-login-banner
DOEMSG_ONELINE=$(%{__cat} %{SOURCE2})
%{__cat} << EOF >> %{buildroot}/etc/dconf/db/distro.d/20-login-banner
### THIS FILE IS MANAGED BY fermilab-conf_doe-banner-gdm ###
###  YOUR CHANGES HERE WILL BE REVERTED BY THIS PACAKGE  ###
[org/gnome/login-screen]
banner-message-text="${DOEMSG_ONELINE}"
EOF

# KDM
# ???

# LXDE
# ???

%files
%defattr(0644,root,root,0755)
%{_datarootdir}/%{name}

%files cockpit
################################################################
# Cockpit
################################################################
%defattr(0644,root,root,0755)


%triggerin -p /bin/bash cockpit -- cockpit

##################### BEGIN Trigger Snippet #########################
set -u
TRIGGER_ON_PACKAGE_NAME='cockpit'
# The following script snippet attempts to classify why we were called:
#  - on first install of either package, RUN_TRIGGER == "Initial"
#  - on upgrade of _THIS_ package, RUN_TRIGGER == "UpgradeSELF"
#  - on upgrade of the TRIGGERON package, RUN_TRIGGER == "UpgradeTRIGGERON"
#  - on upgrade of the TRIGGERON package but initial install of _THIS_ package, RUN_TRIGGER == "InitialSELFUpgradeTRIGGERON"
#  - on upgrade of the BOTH packages, RUN_TRIGGER == "UPGRADEALL"

CURRENT_INSTALLS_OF_THIS_PACKAGE=${1:-0}
TRIGGER_ON_PACKAGE=${2:-0}

RUN_TRIGGER="NO"
if [[ ${TRIGGER_ON_PACKAGE} -eq 1 ]]; then
    # We only get here if we are NOT doing an upgrade of the trigger package
    if [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -eq 0 ]]; then
        # We only get here if we are removing _THIS_ package
        RUN_TRIGGER="UninstallSELF"
    elif [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -eq 1 ]]; then
        # We only get here if we are NOT doing an upgrade of the trigger package
        #                and we are installing _THIS_ package for the first time
        RUN_TRIGGER="Initial"
    elif [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -gt 1 ]]; then
        # We only get here if we are NOT doing an upgrade of the trigger package
        #                and we are upgrading _THIS_ package
        RUN_TRIGGER="UpgradeSELF"
    fi
elif [[ ${TRIGGER_ON_PACKAGE} -gt 1 ]]; then
    # We only get here if we are doing an upgrade of the trigger package
    if [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -eq 1 ]]; then
        # We get here if we are doing an upgrade of the trigger package
        #                     and we are NOT upgrading _THIS_ package
        RUN_TRIGGER="UpgradeTRIGGERON"

        #  But, are we installing _THIS_ package as a part of a dependency
        #       resolution chain?
        _THIS_TID=$(rpm -q --qf "%{INSTALLTID}\n" %{NAME})
        # Find the last installed (ie the current) TRIGGER_ON_PACKAGE_NAME's transaction
        TID=$(rpm -q --qf "%{INSTALLTID}\n" ${TRIGGER_ON_PACKAGE_NAME} --last |grep -v ${TRIGGER_ON_PACKAGE_NAME} | head -1)
        if [[ "${_THIS_TID}" == "${TID}" ]]; then
            # if the transaction ID of _THIS_ package is identical to the
            #  transaction ID of an installed TRIGGER_ON_PACKAGE_NAME
            # then, we must be upgrading the trigger package and
            # installing _THIS_ package
            RUN_TRIGGER="InitialSELFUpgradeTRIGGERON"
        fi
    elif [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -gt 1 ]]; then
        # We only get here if we are doing an upgrade of the trigger package
        #                     and we are upgrading _THIS_ package
        RUN_TRIGGER="UpgradeALL"
    fi
elif [[ ${TRIGGER_ON_PACKAGE} -eq 0 ]]; then
    # We only get here if we are removing the trigger package
    RUN_TRIGGER="UninstallTRIGGERON"
fi

if [[ "${RUN_TRIGGER}" == "NO" ]]; then
    # If we got here if:
    #  some kind of edge case appeared......
    echo "##################################" >&2
    echo "%{NAME}: Not sure what this means"  >&2
    echo "CURRENT_INSTALLS_OF_THIS_PACKAGE = ${CURRENT_INSTALLS_OF_THIS_PACKAGE}"  >&2
    echo "TRIGGER_ON_PACKAGE (${TRIGGER_ON_PACKAGE_NAME}) = ${TRIGGER_ON_PACKAGE}" >&2
    echo "##################################" >&2
    exit 1
fi

##################### End of Trigger Snippet ########################

if [[ "${RUN_TRIGGER}" == "UpgradeTRIGGERON" ]]; then
    # If we got here if:
    #  a) we are upgrading the trigger package, but not _THIS_ package
    #       so we've already run this once and will not run it again.

    # If the user changed the config themselves, we shouldn't undo their work
    #  if we decide we need to, we can always alter the behavior in the next
    #  version of this package.
    exit 0
fi


# the oz.cfg config file is a close enough format for now
# https://github.com/hercules-team/augeas/pull/675
mkdir -p %{_sysconfdir}/cockpit
touch %{_sysconfdir}/cockpit/cockpit.conf

TMPFILE=$(mktemp)
%{__cat} > ${TMPFILE} <<EOF
rm /augeas/load/Oz/incl
set /augeas/load/Oz/incl "%{_sysconfdir}/cockpit/cockpit.conf"
load

set /files/%{_sysconfdir}/cockpit/cockpit.conf/Session/Banner %{_datarootdir}/%{name}/doe_banner_80_char.txt
save
EOF

# capture stdout cleanly
OUT=$(augtool --noload < ${TMPFILE})

rm -f ${TMPFILE}

restorecon -F  %{_sysconfdir}/cockpit/cockpit.conf >/dev/null 2>&1

%preun -p /bin/bash cockpit
if [[ $1 == 0 ]]; then

  if [[ ! -e %{_sysconfdir}/cockpit/cockpit.conf ]]; then
    # config doesn't exist, no need to edit
    exit 0
  fi

  TMPFILE=$(mktemp)
  %{__cat} > ${TMPFILE} <<EOF
rm /augeas/load/Oz/incl
set /augeas/load/Oz/incl "%{_sysconfdir}/cockpit/cockpit.conf"
load

set /files/%{_sysconfdir}/cockpit/cockpit.conf/Session/Banner /etc/motd
save
EOF

  # capture stdout cleanly
  OUT=$(augtool --noload < ${TMPFILE})

  rm -f ${TMPFILE}
  restorecon -F  %{_sysconfdir}/cockpit/cockpit.conf >/dev/null 2>&1
fi


%files console
################################################################
# Console
################################################################
%defattr(0644,root,root,0755)
%if 0%{?rhel} >= 9 || 0%{?fedora} >= 31
/etc/issue.d/doe_banner_80_char.issue
/etc/motd.d/doe_banner_80_char
%else
%post -p /bin/bash
%{__cat} %{_datarootdir}/%{name}/doe_banner_80_char.txt > %{_sysconfdir}/motd
%{__cat} %{_datarootdir}/%{name}/doe_banner_80_char.txt > %{_sysconfdir}/issue
echo > %{_sysconfdir}/issue.net

restorecon -F  %{_sysconfdir}/motd %{_sysconfdir}/issue %{_sysconfdir}/issue.net >/dev/null 2>&1

%{_fixperms} %{_sysconfdir}/motd %{_sysconfdir}/issue %{_sysconfdir}/issue.net

%preun -p /bin/bash
if [[ $1 == 0 ]]; then
  echo > %{_sysconfdir}/motd
  touch %{_sysconfdir}/issue.net  # issue.net has no default content
  
  # put the default back
  %{__cat} > %{_sysconfdir}/issue <<EOF
\S
Kernel \r on an \m
EOF

  restorecon -F  %{_sysconfdir}/motd %{_sysconfdir}/issue %{_sysconfdir}/issue.net >/dev/null 2>&1

  %{_fixperms} %{_sysconfdir}/motd %{_sysconfdir}/issue %{_sysconfdir}/issue.net
fi
%endif

%files login-screen
################################################################
# login-screen
################################################################
%defattr(0644,root,root,0755)

%files gdm
################################################################
# gdm
################################################################
%defattr(0644,root,root,0755)
%config /etc/dconf/db/distro.d/locks/20-login-banner
%config /etc/dconf/db/distro.d/20-login-banner

%post -p /bin/bash gdm
dconf update
%postun -p /bin/bash gdm
dconf update


%changelog
* Wed Mar 16 2022 Pat Riehecky <riehecky@fnal.gov> 1.0-5
- now that motd and agetty support `.d` bits in EL9, break these out
- Unify the various related packages into one spec with subpackages
