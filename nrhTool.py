#Maya Rigging Toolset
#by Nate Hancock
#updated 06_08_2021

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

def gui(): 
    win='myUI'
    if cmds.window(win,ex=True):
        cmds.deleteUI(win)

    cmds.window(win, mm=True)
    cmds.backgroundColor=(1.0, 0.0, 0.5)
    cmds.docTag='Rigging'
    cmds.columnLayout('Main', cal='left')
    cmds.button(w=300,l='Create Square Icon',c=nrhSquare)
    cmds.button(w=300,l='Custom Star Icon',c=nrhCustom)
    cmds.button(w=300,l='Create Cube Icon',c=nrhCube)
    cmds.button(w=300,l='Mirror Selected Joint',c=nrhMirrorjoint)
    cmds.button(w=300,l='Create Control on Selected',c=create_icon)
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
    cmds.button(w=300,l='Quick arm system rig', c=nrhArm)
    cmds.button(w=300,l='Complex Space Switching Quick Setup', c=nrhSwitch)
    cmds.button(w=300,l='Create Quick FK Menu',c=nrhFk)
    cmds.button(w=300,l='Auto Rig Joint Chain w/ Pads',c=nrhAutoRig)
    cmds.button(w=300,l='Create Hand Attributes on Selected Object',c=nrhHands)
    cmds.button(w=300,l='Create Face Attribtes', c=nrhFace)
    cmds.button(w=300,l='Close',c=nrhWin)
    cmds.showWindow()

# gui button functions
def nrhJoint(*args):
    cmds.joint(p=(0,0,0))
    cmds.joint(p=(2,0,0))
    cmds.joint('joint1',e=True,zso=True,oj='xyz')
    cmds.joint(p=(4,0,0))
    cmds.joint('joint2',e=True,zso=True,oj='xyz')

def nrhArm(*args):
    import nrhAutoJoints_v1
    reload(nrhAutoJoints_v1)
    nrhAutoJoints_v1.armGui()

def create_icon(*args):
    current_joint = pm.ls(sl=True)
    star = pm.circle(name='x_ctrl',c=[0,0,0],nr=[0,1,0],sw=360,r=1,d=3,ut=0,tol=0.01,s=16,ch=1)[0]
    
    print star
    
    pm.xform(star.cv[0::4], s=[3.5,3.5,3.5], ro=[0,22.5,0])
    pm.xform(star, ro=[90,0,0], s=[2,2,2])
    nrhCleanup()
    
    proxy_group = pm.group(star, n='x_ctrl_offset')
    
    trash_contraint = pm.parentConstraint(current_joint, proxy_group, mo=False)
    
    pm.delete(trash_contraint)
    pm.parentConstraint(star, current_joint)
    print ('Control has been placed.')

#function for quick cleanup
def nrhCleanup():
    sel = pm.ls(selection = True)
    for obj in sel:
        pm.xform(obj, centerPivots = True)   
        pm.delete(constructionHistory=True)  
        pm.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        pm.select(d=True)
    print "Object's Cleaned"

def nrhCustom(*args):
    star = pm.circle(name='star_ctrl',c=[0,0,0],nr=[0,1,0],sw=360,r=1,d=3,ut=0,tol=0.01,s=16,ch=1)[0]
    print star

    pm.xform(star.cv[0::2], s=[3,3,3])

def nrhMirrorjoint(*args):
    pm.mirrorJoint(mirrorBehavior=1, mirrorYZ=1, searchReplace=("lt", "rt"))

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

def nrhSwitch(*args):
    import spaceswitchTool_setup
    reload(spaceswitchTool_setup)

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
    ctrl.addAttr('Thumb_twist', k=1, min=-10, max=10)
    ctrl.addAttr('Thumb_spread', k=1, min=-10, max=10)

def nrhFace(*args):
    ctrl=pm.ls(sl=1)[0]

    ctrl.addAttr('faceBlends', k=1, at='enum', en='----------:')
    ctrl.addAttr('mouthAll', k=1, at='enum', en='-----:')
    ctrl.addAttr('ltSmile', k=1, min=0, max=10)
    ctrl.addAttr('rtSmile', k=1, min=0, max=10)
    ctrl.addAttr('mouthSmile', k=1, min=0, max=10)
    ctrl.addAttr('ltFrown', k=1, min=0, max=10)    
    ctrl.addAttr('rtFouth', k=1, min=0, max=10)   
    ctrl.addAttr('mouthFrown', k=1, min=0, max=10)
    ctrl.addAttr('ltWide', k=1, min=0, max=10)
    ctrl.addAttr('rtWide', k=1, min=0, max=10)
    ctrl.addAttr('mouthWide', k=1, min=0, max=10)    
    ctrl.addAttr('lips', k=1, min=0, max=10)
    ctrl.addAttr('ouShape', k=1, min=0, max=10)
    ctrl.addAttr('thShape', k=1, min=0, max=10)
    ctrl.addAttr('mouthPurse', k=1, min=0, max=10)
    ctrl.addAttr('eyes', k=1, at='enum', en='-----:')
    ctrl.addAttr('blink', k=1, min=0, max=10)
    ctrl.addAttr('ltBlink', k=1, min=0, max=10)
    ctrl.addAttr('rtBlink', k=1, min=0, max=10)

def nrhWin(*args):
    cmds.deleteUI('myUI')
    cmds.window(thanks, w=800, h=350)
    cmds.columnLayout( adjustableColumn=True)
    cmds.text(label='Thanks for using my toolset')
    cmds.text(label='I hope you enjoyed',align='center')
    cmds.text(label='By Nate Hancock',align='center')
    cmds.text(label='First created Jan 2021',align='right')
    cmds.text(label='Updated June 2021 V2.008',align='right')
    cmds.showWindow()
