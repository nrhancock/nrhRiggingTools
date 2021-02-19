#Maya Rigging Toolset
#by Nate Hancock
#See PEP 8 styleguide for consistency



import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
print "ThaBossSawzz"



def gui(): 
    win='myUI'
    if cmds.window(win,ex=True):
        cmds.deleteUI(win)

    cmds.window(win)
    cmds.backgroundColor=(1.0, 0.0, 0.5)
    cmds.docTag='Rigging'
    cmds.columnLayout('Main')
    cmds.button(w=300,l='Create Square Icon',c=nrhSquare)
    cmds.button(w=300,l='Custom Star Icon',c=nrhCustom)
    cmds.button(w=300,l='Create Cube Icon',c=nrhCube)
    cmds.button(w=300,l='Quick Cleanup',c=nrhQuicky)
    cmds.rowColumnLayout(nc=2)
    cmds.button(w=150,l='Freeze Transforms',c=nrhFreeze)
    cmds.button(w=150,l='Delete History',c=nrhHistory)
    cmds.button(w=150,l='Center Pivot',c=nrhCenter)
    cmds.button(w=150,l='Empty Group',c=nrhGroup)
    cmds.setParent('Main')
    cmds.rowColumnLayout(nc=2)
    global pre
    pre=cmds.textField(w=100)
    cmds.button(w=100,l='Prefix',c=nrhPre)
    global suf
    suf=cmds.textField(w=100)
    cmds.button(w=100,l='Suffix',c=nrhSuf)
    global ren
    ren=cmds.textField(w=100)
    cmds.button(w=100,l='Rename',c=nrhRen)
    cmds.setParent('Main')
    cmds.docTag='Rigging'
    cmds.button(w=300,l='Create Quick FK Menu',c=nrhFk)
    cmds.button(w=300,l='Auto Rig Joint Chain w/ Pads',c=nrhAutoRig)
    cmds.button(w=300,l='Create Hand Attriburtes on Selected Object',c=nrhHands)
    cmds.button(w=300,l='Close',c=nrhWin)
    cmds.showWindow()



# gui button functions
def nrhJoint(*args):
    cmds.joint(p=(0,0,0))
    cmds.joint(p=(2,0,0))
    cmds.joint('joint1',e=True,zso=True,oj='xyz')
    cmds.joint(p=(4,0,0))
    cmds.joint('joint2',e=True,zso=True,oj='xyz')
    '''
    next project on this is learning how and utilizing the limitSwitch
    commands to limit joint rotation on specific reigons
    here:http://help.autodesk.com/view/MAYAUL/2019/ENU/index.html?contextId=COMMANDSPYTHON-INDEX
   '''




def nrhCustom(*args):
    star = pm.circle(name='star_ctrl',c=[0,0,0],nr=[0,1,0],sw=360,r=1,d=3,ut=0,tol=0.01,s=16,ch=1)[0]
    print star

    pm.xform(star.cv[0::2], s=[3,3,3])




def nrhSquare(*args):
    ctrl = pm.circle(name='square_ctrl',c=[0,0,0],nr=[0,1,0],sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1)[0]
    print ctrl

    pm.xform(ctrl.cv[0::2], s=[2,2,2])




def nrhQuicky(*args):
    sel = cmds.ls(selection = True)
    for obj in sel:
        cmds.xform(obj, centerPivots = True)
    
    cmds.delete(constructionHistory=True)
    
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)



    
def nrhHistory(*args):
    cmds.delete(constructionHistory=True)




def nrhFreeze(*args):
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0) 



    
def nrhCenter(*args):
    sel = cmds.ls(selection = True)
    for obj in sel:
        cmds.xform(obj, centerPivots = True)




def nrhGroup(*args):
    cmds.group( em=True, name='null1' )




def nrhPre(*args):
    nrhPrefix=cmds.textField(pre,q=True,text=True)
    
    oldName=cmds.ls(sl=True)
    
    for old in oldName:
        newName = nrhPrefix + '_' +old
        cmds.rename(old,newName)




def nrhSuf(*args):
    nrhSuffix=cmds.textField(suf,q=True,text=True)
    
    oldName=cmds.ls(sl=True)
    
    for old in oldName:
        newName = old + '_' +nrhSuffix
        cmds.rename(old,newName)



     
def nrhRen(*args):
    nrhRename=cmds.textField(ren,q=True,text=True)
    
    oldName=cmds.ls(sl=True)
    
    for old in oldName:
        newName = nrhRename
        cmds.rename(newName)




def nrhCube(*args):
    mel.eval("source nurbCube;")




def nrhFk(*args):
	mel.eval("source makeFKControls_withScale;")
	mel.eval("makeFKControls_withScale;")




def nrhAutoRig(*args):
    joint_chain = pm.ls(sl=True, dag=True)
    last_icon = None
    control_icons = []
    for current_joint in joint_chain[0:-1]:
        print current_joint
        current_icon = pm.circle(radius=4, normal=[1, 0, 0])[0]
        local_pad = pm.group()
        waste_icon = pm.parentConstraint(current_joint, local_pad)
        pm.delete(waste_icon)
        
        if last_icon:
            pm.parent(local_pad, last_icon)
        
        #connect the control back to the joint
        pm.orientConstraint(current_icon, current_joint)
        
        last_icon = current_icon
        
        control_icons.append(current_icon)
        
    pm.select(control_icons, r=True)




def nrhHands(*args):
    ctrl=pm.ls(sl=1)[0]

    ctrl.addAttr('Hand', k=1, at='enum', en='----------:')
    ctrl.addAttr('Fist', k=1, min=-10, max=10)
    ctrl.addAttr('Spread', k=1, min=-10, max=10)
    ctrl.addAttr('Fingers', k=1, at='enum', en='-----:')
    ctrl.addAttr('Index_curl', k=1, min=-10, max=10)
    ctrl.addAttr('Index_twist', k=1, min=-10, max=10)
    ctrl.addAttr('Middle_curl', k=1, min=-10, max=10)
    ctrl.addAttr('Middle_twist', k=1, min=-10, max=10)
    ctrl.addAttr('Ring_curl', k=1, min=-10, max=10)
    ctrl.addAttr('Ring_twist', k=1, min=-10, max=10)
    ctrl.addAttr('Pinky_curl', k=1, min=-10, max=10)
    ctrl.addAttr('Pinky_twist', k=1, min=-10, max=10)
    ctrl.addAttr('Thumb', k=1, at='enum', en='-----:')
    ctrl.addAttr('Thumb_curl', k=1, min=-10, max=10)
    ctrl.addAttr('Thumb_twist', k=1, min=-10, max=101)
    ctrl.addAttr('Thumb_spread', k=1, min=-10, max=10)




#credits
lock='Roll the Credits'
trash='Credits'
thanks='Thank You'
splash='Dialog'

def nrhWin(*args):
    if cmds.window('myUI',ex=True):
        cmds.deleteUI('myUI')

    cmds.window(thanks, w=800, h=350)
    cmds.columnLayout( adjustableColumn=True)
    cmds.text(label='Thanks for using my toolset')
    cmds.text(label='I hope you enjoyed',align='center')
    cmds.text(label='By Nate Hancock',align='center')
    cmds.text(label='First created Jan 2021',align='right')
    cmds.text(label='Updated Feb 2021 V2.004',align='right')
    cmds.showWindow()

#creditsendhere


