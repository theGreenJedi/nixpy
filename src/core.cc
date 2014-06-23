#include <boost/python.hpp>
#include <boost/optional/optional.hpp>

#include <nix.hpp>
#include <transmorgify.hpp>
#include <accessors.hpp>

#include <PyEntity.hpp>
#include <PyBlock.hpp>
#include <PyFile.hpp>

using namespace boost::python;
using namespace nix;
using namespace base;
using namespace nixpy;

static void
nix_data_array_label_setter ( DataArray &da, const boost::optional<std::string> &lbl ) {
    if ( lbl == boost::none ) {
        da.label ( boost::none );
    } else {
        da.label ( *lbl );
    }
}


BOOST_PYTHON_MODULE(core)
{
    PyFile::do_export();

    class_<Value>("Value");
    to_python_converter<std::vector<Value>, vector_transmogrify<Value>>();
    to_python_converter<boost::optional<Value>, option_transmogrify<Value>>();

    class_<Property>("Property");
    to_python_converter<std::vector<Property>, vector_transmogrify<Property>>();
    to_python_converter<boost::optional<Property>, option_transmogrify<Property>>();

    PyNamedEntity<ISection>::do_export("Section");
    class_<Section, bases<NamedEntity<ISection>>>("Section")
        .def("__str__", &toStr<Section>)
        .def("__repr__", &toStr<Section>)
        .def(self == self);
    to_python_converter<std::vector<Section>, vector_transmogrify<Section>>();
    to_python_converter<boost::optional<Section>, option_transmogrify<Section>>();

    PyBlock::do_export();

    PyEntityWithMetadata<ISource>::do_export("Source");
    class_<Source, bases<EntityWithMetadata<ISource>>>("Source")
        .def("__str__", &toStr<Source>)
        .def("__repr__", &toStr<Source>)
        .def(self == self);
    to_python_converter<std::vector<Source>, vector_transmogrify<Source>>();
    to_python_converter<boost::optional<Source>, option_transmogrify<Source>>();

    PyEntityWithSources<IDataArray>::do_export("DataArray");
    class_<DataArray, bases<EntityWithSources<IDataArray>>>("DataArray")
        .add_property("label",
                      OPT_GETTER(std::string, DataArray, label),
                      &nix_data_array_label_setter)
        .def("has_data", &DataArray::hasData)
        ;


    to_python_converter<std::vector<DataArray>, vector_transmogrify<DataArray>>();
    vector_transmogrify<DataArray>::register_from_python();
    to_python_converter<boost::optional<DataArray>, option_transmogrify<DataArray>>();


    // TODO enum class DataType

    class_<Dimension>("Dimension");

    class_<SampledDimension>("SampledDimension");

    class_<RangeDimension>("RangeDimension");

    class_<SetDimension>("SetDimension");

    PyEntityWithSources<ISimpleTag>::do_export("SimpleTag");
    class_<SimpleTag, bases<EntityWithSources<ISimpleTag>>>("SimpleTag");
    to_python_converter<std::vector<SimpleTag>, vector_transmogrify<SimpleTag>>();
    to_python_converter<boost::optional<SimpleTag>, option_transmogrify<SimpleTag>>();

    PyEntityWithSources<IDataTag>::do_export("DataTag");
    class_<DataTag, bases<EntityWithSources<IDataTag>>>("DataTag");
    to_python_converter<std::vector<DataTag>, vector_transmogrify<DataTag>>();
    to_python_converter<boost::optional<DataTag>, option_transmogrify<DataTag>>();

    class_<Feature>("Feature");

    // TODO enum class LinkType

    to_python_converter<boost::optional<std::string>, option_transmogrify<std::string>>();
    option_transmogrify<std::string>::register_from_python();
}
