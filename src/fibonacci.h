class GeomProgression: public Progression {
public:
   GeomProgression(long b = 2);
protected:
	virtual long nextValue()
protected:
    long base;
};
GeomProgression::GeomProgression(long b)
: Progression(1), base(b) {}
long GeomProgression::nextValue(){
cur *=base;
return cur;
}
