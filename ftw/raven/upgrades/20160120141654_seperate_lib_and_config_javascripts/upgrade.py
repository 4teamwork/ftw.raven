from ftw.upgrade import UpgradeStep


class SeperateLibAndConfigJavascripts(UpgradeStep):
    """Seperate lib and config javascripts.
    """

    def __call__(self):
        self.install_upgrade_profile()
