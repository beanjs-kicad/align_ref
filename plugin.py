import wx
import pcbnew

from os import path
from pcbnew import ActionPlugin, GetBoard


class AlignRefPlugin(ActionPlugin):
    def defaults(self):
        cwd = path.dirname(__file__)

        self.name = "Align Ref"
        self.category = "Modify PCB"
        self.description = "Copyright @ beanjs"
        self.icon_file_name = path.join(cwd, 'icon.png')
        self.show_toolbar_button = True
        self.logger = open(path.join(cwd, "logger.txt"), "w+")

    def Run(self):
        board = GetBoard()
        footprints = board.GetFootprints()
        designSettings = board.GetDesignSettings()

        for fp in footprints:
            fpLayerId = fp.GetLayer()

            ref = fp.Reference()
            # layerId=ref.GetLayer()

            if fpLayerId == pcbnew.F_Cu:
                designLayerId = pcbnew.F_SilkS
                refLayerId = pcbnew.User_1
            elif fpLayerId == pcbnew.B_Cu:
                designLayerId = pcbnew.B_SilkS
                refLayerId = pcbnew.User_2

            textSize = designSettings.GetTextSize(designLayerId)
            # self.logger.writelines([textSize, refLayerId])

            ref.SetLayer(refLayerId)
            ref.SetTextThickness(
                designSettings.GetTextThickness(designLayerId))
            ref.SetTextWidth(textSize.GetWidth())
            ref.SetTextHeight(textSize.GetHeight())
            # ref.SetTextAngle(0)

            fpCenter = self.GetFPCenter(fp)
            if fpCenter is None:
                ref.SetVisible(False)
            else:
                ref.SetPosition(fpCenter)

        wx.MessageBox("align finished!!")
        pcbnew.Refresh()

    def GetFPCenter(self, fp):
        fpLayerId = fp.GetLayer()

        ctrLayerId = pcbnew.F_CrtYd
        if fpLayerId == pcbnew.B_Cu:
            ctrLayerId = pcbnew.B_CrtYd

        gItems = fp.GraphicalItems()

        minx = 1000000000000
        miny = 1000000000000
        maxx = -1
        maxy = -1
        for item in gItems:
            if item.GetLayer() == ctrLayerId:
                iBox = item.GetBoundingBox()
                if iBox.GetLeft() < minx:
                    minx = iBox.GetLeft()

                if iBox.GetRight() > maxx:
                    maxx = iBox.GetRight()

                if iBox.GetTop() < miny:
                    miny = iBox.GetTop()

                if iBox.GetBottom() > maxy:
                    maxy = iBox.GetBottom()

        if maxx == -1 or maxy == -1 or minx == 1000000000000 or miny == 1000000000000:
            return None

        return pcbnew.VECTOR2I(int((minx+maxx)/2), int((miny+maxy)/2))
