from api.predict import load_model, chat

model = load_model()

print("Test prompt with simple context.")
response = chat(model, "Tell me about Wainamoinen.", context="Context:\nVäinämöinen is a wise old bard.\n")
print(response)


print("\nTest prompt with more advanced context.")
response = chat(
    model,
    "Tell me about Wainamoinen.",
    context="""To these regions unbefitting;
Happy was I with my kindred,
In my distant home and country,
There my name was named in honor.”
Louhi,hostess of Pohyola,
Thus replied to Wainamoinen:
“I would gain the information,
ShouldI be allowed to ask thee,
Who thou art of ancient heroes,
Who of all the host of heroes?”
This is Wainamoinen’s answer:
“Formerly my name was mentioned,
Often was I heard and honored,
As a minstrel and magician,
In the long and drearywinters,
Calledthe Singerof the Northland,
In the valleys of Wainola,
On the plainsof Kalevala;
No one thought that such misfortune
Could befallwise Wainamoinen.”
Louhi,hostess of Pohyola,
Thus replied in cheering accents:
“Rise,O hero, from discomfort,
From thy bed among the willows;
Enter now upon the new-way,
Come with me to yonderdwelling,

Wainamoinen, old and faithful,
Thus addressed the new-made vessel:
“Go, thou boat of master-magic,
Hastento the willing waters,
Speed away upon the blue-sea,
And without the hand to move thee;
Let my will impel thee seaward.”
Quick the boat rolledto the billows
On the cylinders of oak-wood,
Quick descended to the waters,
Willingly obeyedhis master.
Wainamoinen, the magician,
Then began to rake the sea-beds,
Raked up all the water-flowers,
Bits of brokenreeds and rushes,
Deep-sea shellsand colored pebbles,
Did not find his harp of fish-bone,
Lost forever to Wainola!
Thereupon the ancient minstrel
Left the waters, homeward hastened,
Cap pulleddown upon his forehead,
Sang this song with sorrowladen:
“Nevermore shall I awaken
With my harp-strings, joy and gladness!
Nevermore will Wainamoinen

On thy hands,the glovesof Mana;
Tell the truth now, Wainamoinen,
What has brought thee to Manala?”
Wainamoinen, artfulhero,
Gives this answer, still finessing:
“Iron brought me to Manala,
To the kingdom of Tuoni.”
Speaksthe virginof the death-land,
Mana’swise and tiny daughter:
“Well I know that this is falsehood)
"""
)
print(response)
