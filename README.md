# PDA-NPDA-String-Acceptance-Simulator-Theory-of-Languages-and-Automata-Project 

This repository contains the implementation of a simulator for Pushdown Automata (PDA) and Non-deterministic Pushdown Automata (NPDA). The goal of this project was to verify whether a given string is accepted by a user-defined PDA or NPDA over an independent formal language.

# 🧠 Features and Workflow

The simulator guides the user through defining and testing a PDA/NPDA with the following steps:

Input the set of states

Input the input alphabet

Input the stack alphabet

Input the transition rules

Define the start state

Define the initial stack symbol

Define the set of accepting states

Enter the input string

Step-by-step simulation:

Displays the current input symbol, stack content, and active state at each step

Continues until the input is fully processed or the automaton halts

Final result: Accepts or rejects the string based on the transition path

# ⚙️ Technical Details
 Language: python using kivy framework

 Designed to support both PDA and NPDA

 No λ (epsilon) transitions are allowed to simplify parsing logic

 Error handling is enforced to avoid crashes

 No use of external automata libraries (e.g., no direct simulator libraries)

 Optional: GUI implementation for a better user experience (if implemented)

# 📈 Optional Bonus Features (fully implemented)
 Graphical User Interface (GUI)

 PDA/NPDA visualization per step

 Multiple path exploration for NPDA

 Clear error messages for malformed input or invalid transitions

